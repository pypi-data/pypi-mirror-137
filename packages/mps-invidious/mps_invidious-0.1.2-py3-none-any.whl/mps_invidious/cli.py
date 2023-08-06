import atexit
import json
import os.path
import random
import re
import readline
import socket
import subprocess
import tempfile
import time
from datetime import timedelta
from enum import IntEnum

from appdirs import AppDirs
from rich.columns import Columns
from rich.console import Console
from rich.table import Table
from rich.text import Text

import mps_invidious
from mps_invidious.api import HttpError, InvidiousClient
from mps_invidious.util import StrEnum, strfdelta

EXIT_COMMANDS = (
    'exit',
)


class PlayerEvent(StrEnum):
    ELAPSED = 'elapsed'
    VOLUME = 'volume'


class PlayerEventId(IntEnum):
    ELAPSED = 1
    VOLUME = 2


class PlayerExitCode(IntEnum):
    NEXT = 0
    PREV = 42
    STOP = 43


def get_formatted_duration(seconds):
    length = timedelta(seconds=seconds)
    return strfdelta(length)


def make_search_result_line(index, result, style):
    length_str = get_formatted_duration(result["lengthSeconds"])

    return [
        Text(str(index), style=style),
        Text(result['title'], style=style),
        Text(result['videoId'], style=style),
        Text(length_str, style=style),
    ]


def setup_readlines():
    dirs = AppDirs(mps_invidious.NAME)

    readline.set_history_length(1000)

    try:
        os.makedirs(dirs.user_data_dir)
    except FileExistsError:
        pass

    history_path = os.path.join(dirs.user_data_dir, 'history')
    try:
        readline.read_history_file(history_path)
    except FileNotFoundError:
        open(history_path, 'wb').close()
        history_len = 0
    else:
        history_len = readline.get_current_history_length()

    def save(prev_h_len, history_path):
        new_h_len = readline.get_current_history_length()
        readline.set_history_length(1000)
        readline.append_history_file(new_h_len - prev_h_len, history_path)

    atexit.register(save, history_len, history_path)


def search(*, client, query, target):
    results = []

    page_results = ['']

    page = 0
    while page_results and len(results) < target:
        page_results = client.search(query, page=page)
        results += page_results

        page += 1

    return results[:target]


def fetch_socket_data(process, socket_path):
    s = socket.socket(socket.AF_UNIX)

    tries = 0
    while tries < 10 and process.poll() is None:
        time.sleep(.5)
        try:
            s.connect(socket_path)
            break
        except socket.error:
            pass
        tries += 1
    else:
        return

    try:
        cmd = {"command": ["observe_property", 1, "time-pos"]}
        s.send(json.dumps(cmd).encode() + b'\n')
        volume = elapsed = None

        for line in s.makefile():
            resp = json.loads(line)
            new_volume = new_elapsed = None

            if (
                resp.get('event') == 'property-change' and
                resp['id'] == PlayerEventId.ELAPSED and
                resp['data'] is not None
            ):
                new_elapsed = int(resp['data'])

            elif (
                resp.get('event') == 'property-change' and
                resp['id'] == PlayerEventId.VOLUME
            ):
                new_volume = int(resp['data'])

            if new_elapsed and new_elapsed != elapsed:
                elapsed = new_elapsed
                yield PlayerEvent.ELAPSED, elapsed

            if new_volume and new_volume != volume:
                volume = new_volume
                yield PlayerEvent.VOLUME, volume

    except socket.error:
        pass


INDEX_RANGE_RE = r'(\*|((\d+)(-\d+)?))'
INDEX_EXPRESSION_RE = re.compile(fr'^({INDEX_RANGE_RE},)*{INDEX_RANGE_RE}$')


def parse_index_expression_gen(expression, total_results):
    for segment in expression.split(','):
        segment_parts = segment.split('-')

        if len(segment_parts) == 1:
            [element] = segment_parts
            if element == '*':
                yield from range(total_results)
            else:
                yield int(element)

        elif len(segment_parts) == 2:
            left, right = map(int, segment_parts)
            yield from range(left, right + 1)

        else:
            assert False, (expression, segment, segment_parts)


def is_index_expression(line):
    return bool(INDEX_EXPRESSION_RE.match(line))


def _get_input_file():
    dirs = AppDirs("mpv")
    confpath = conf = ''

    confpath = os.path.join(dirs.user_config_dir, "mpv-input.conf")

    if os.path.isfile(confpath):
        with open(confpath) as conffile:
            conf = conffile.read() + '\n'

    conf = conf.replace("quit", f"quit {PlayerExitCode.STOP}")
    conf = conf.replace("playlist_prev", f"quit {PlayerExitCode.PREV}")
    conf = conf.replace("pt_step -1", f"quit {PlayerExitCode.PREV}")
    conf = conf.replace("playlist_next", "quit")
    conf = conf.replace("pt_step 1", "quit")
    standard_cmds = [
        f'q quit {PlayerExitCode.STOP}\n',
        '> quit\n',
        f'< quit {PlayerExitCode.PREV}\n',
        'NEXT quit\n',
        f'PREV quit {PlayerExitCode.PREV}\n',
        'ENTER quit\n',
    ]
    bound_keys = [i.split()[0] for i in conf.splitlines() if i.split()]

    for i in standard_cmds:
        key = i.split()[0]

        if key not in bound_keys:
            conf += i

    with tempfile.NamedTemporaryFile(
        'w',
        prefix='mps-invidious-input',
        suffix='.conf',
        delete=False
    ) as tmpfile:
        tmpfile.write(conf)

    return tmpfile.name


def delete_file_path(file_path):
    def inner():
        if os.path.exists(file_path):
            os.unlink(file_path)

    return inner


class CliCommand:
    def __init__(self, cli):
        self.cli = cli

    def match(self, command):
        return False

    def run(self):
        pass


class Search(CliCommand):
    def match(self, command):
        return command.startswith('/')

    def run(self, command):
        self.cli.reset_results()
        self.cli.refresh_screen('')

        self.cli.console.print('> … Searching …', end='')

        try:
            self.cli.results = search(
                client=self.cli.client,
                query=command[1:],
                target=self.cli.console.size.height - 1,
            )
        except HttpError as exc:
            self.cli.results = []
            message = f'Error searching results: {exc.status_code}'
        else:
            message = ''

        self.cli.console.print()
        self.cli.refresh_screen(message)


class Play(CliCommand):
    def match(self, command):
        return is_index_expression(command)

    def _get_all_indexes(self, command):
        return list(
            parse_index_expression_gen(
                command,
                len(self.cli.results),
            ),
        )

    def run(self, command):
        all_indexes = self._get_all_indexes(command)

        for index in all_indexes:
            try:
                self.cli.results[index]
            except IndexError:
                self.cli.refresh_screen(f'Invalid index: {index}')
                return

        i = 0
        while 0 <= i < len(all_indexes):
            index = all_indexes[i]

            self.cli.playing_index = index

            result = self.cli.results[index]
            exit_code = self.play(
                video_id=result['videoId'],
                title=result['title'],
            )

            if exit_code == PlayerExitCode.STOP:
                break
            else:
                i = self.get_next_index(
                    index=i,
                    exit_code=exit_code,
                    all_indexes_count=len(all_indexes),
                )

        self.cli.playing_index = None
        self.cli.refresh_screen('')

    def get_next_index(self, *, index, exit_code, all_indexes_count):
        if exit_code == PlayerExitCode.PREV:
            return index - 1
        elif exit_code == PlayerExitCode.NEXT:
            return index + 1
        else:
            # TODO: log error?
            return index + 1

    def play(self, video_id, title):
        self.cli.refresh_screen(f'Playing: {title}')

        result = self.cli.client.videos(video_id)
        title = result['title']

        stream_url = result['formatStreams'][0]['url']

        socket_path = tempfile.NamedTemporaryFile(
            prefix='mps-invidious-mpv',
            suffix='.sock',
        ).name
        self.cli.on_exit.append(delete_file_path(socket_path))

        config_file_path = _get_input_file()
        self.cli.on_exit.append(delete_file_path(config_file_path))

        command = [
            'mpv',
            '--no-video',
            '--really-quiet',
            f'--input-unix-socket={socket_path}',
            f'--input-conf={config_file_path}',
            stream_url,
        ]

        process = subprocess.Popen(
            command,
            shell=False,
            stderr=subprocess.DEVNULL,
            bufsize=1,
        )

        duration = get_formatted_duration(result["lengthSeconds"])

        for key, value in fetch_socket_data(process, socket_path):
            if key == PlayerEvent.ELAPSED:
                value_str = get_formatted_duration(value)

                columns = Columns(
                    (
                        f'Playing: {title}',
                        Text(
                            f'{value_str} / {duration}',
                            justify='right',
                            style='bold bright_green',
                        ),
                    ),
                    expand=True,
                )
                self.cli.refresh_screen(columns)

            elif key == PlayerEvent.VOLUME:
                self.cli.console.print('Volume:', value)

            else:
                assert False

        exit_code = process.wait()
        return exit_code


class Loop(Play):
    def match(self, command):
        try:
            head, tail = command.split(' ', maxsplit=-1)
        except ValueError:
            return False
        else:
            return head == 'loop' and super().match(tail)

    def get_next_index(self, *, index, exit_code, all_indexes_count):
        if exit_code == PlayerExitCode.PREV:
            return index - 1 if index > 0 else all_indexes_count - 1
        elif exit_code == PlayerExitCode.NEXT:
            return index + 1 if index < all_indexes_count - 1 else 0
        else:
            # TODO: log error?
            return index + 1 if index < all_indexes_count - 1 else 0

    def _get_all_indexes(self, command):
        _, tail = command.split(' ', maxsplit=-1)
        return super()._get_all_indexes(tail)


class Shuffle(Play):
    def match(self, command):
        return command == 'shuffle'

    def run(self, command):
        random.shuffle(self.cli.results)
        self.cli.refresh_screen('')


class Cli:
    def __init__(self):
        self.client = InvidiousClient()
        self.console = Console()
        self.results = []
        self.playing_index = None

        setup_readlines()

        self.on_exit = []
        atexit.register(self.do_on_exit)

        self.cli_commands = tuple(
            cli_command(self)
            for cli_command in (Search, Play, Shuffle, Loop)
        )

    def do_on_exit(self):
        for x in self.on_exit:
            x()

    def run(self):
        with self.console.screen(hide_cursor=False):
            self._run()

    def refresh_screen(self, status_line):
        self.print_results_table()
        self.print_status_line(status_line)

    def _run(self):
        command = None

        self.refresh_screen('')

        while command not in EXIT_COMMANDS:
            try:
                command = self.console.input('> ')
            except EOFError:
                command = 'exit'

            if command in EXIT_COMMANDS:
                pass

            else:
                for cli_command in self.cli_commands:
                    if cli_command.match(command):
                        cli_command.run(command)
                        break
                else:
                    self.refresh_screen(f'Invalid command: {command}')

    def print_results_table(self):
        def get_style(i):
            if i % 2 == 0:
                style = 'red'
            else:
                style = 'green'

            if i == self.playing_index:
                style = f'{style} on dark_blue'

            return style

        lines = [
            make_search_result_line(i, result, style=get_style(i))
            for i, result in enumerate(self.results)
        ]

        table = Table.grid(expand=True)
        table.add_column("Num")
        table.add_column("Title")
        table.add_column("Video ID")
        table.add_column("Duration", justify="right")

        rows = self.console.size.height
        max_results = rows - 2

        for line in lines[:max_results]:
            table.add_row(*line)

        self.console.print(table)

        for _ in range(len(lines), max_results):
            self.console.print()

    def print_status_line(self, line):
        self.console.print(line, style='cyan')

    def reset_results(self):
        self.results = []


def main():
    Cli().run()


if __name__ == '__main__':
    main()

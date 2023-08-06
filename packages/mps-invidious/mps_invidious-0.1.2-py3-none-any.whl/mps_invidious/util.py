from enum import Enum
from string import Template


class StrEnum(str, Enum):
    pass


class DeltaTemplate(Template):
    delimiter = "%"


def strfdelta(tdelta, fmt='%M:%S'):
    d = {"D": tdelta.days}
    minutes, seconds = divmod(tdelta.seconds, 60)
    d["M"] = '{:02d}'.format(minutes)
    d["S"] = '{:02d}'.format(seconds)
    t = DeltaTemplate(fmt)
    return t.substitute(**d)

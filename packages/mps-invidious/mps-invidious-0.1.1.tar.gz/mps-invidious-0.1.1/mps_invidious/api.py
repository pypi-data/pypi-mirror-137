import urllib.parse

import requests

from mps_invidious.util import StrEnum


class HttpError(requests.exceptions.HTTPError):
    pass


class SortBy(StrEnum):
    DATE = 'date'
    NEWEST = 'newest'
    OLDEST = 'oldest'
    POPULAR = 'popular'
    RATING = 'rating'
    RELEVANCE = 'relevance'
    UPLOAD_DATE = 'upload_date'
    VIEWS = 'views'
    VIEW_COUNT = 'view_count'


class InvidiousClient:
    BASE_URL = 'https://vid.puffyan.us/api/v1/'

    def _request(self, path):
        url = urllib.parse.urljoin(self.BASE_URL, path)
        response = requests.get(url)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            raise HttpError(args=exc.args)

        return response.json()

    def videos(self, video_id):
        return self._request(f'videos/{video_id}')

    def search(self, q, page=0):
        query = urllib.parse.urlencode({
            'q': q,
            'page': page,
            'sort_by': SortBy.RELEVANCE.value
        })
        return self._request(f'search?{query}')


#         self._title = response['title']
#         self._author = response['author']
#         self._rating = response['rating']
#         self._length = response['lengthSeconds']
#         self._viewcount = response['viewCount']

#         self._likes = response['likeCount']
#         self._dislikes = response['dislikeCount']
#         self._username = ['authorId']
#         self._bestthumb = response['thumbnails'][0]['url']

#         # self._category = ['categories'][0] if ['categories'] else ''
#         # self._bigthumb = g.urls['bigthumb'] % self.videoid
#         # self._bigthumbhd = g.urls['bigthumbhd'] % self.videoid
#         # self.expiry = time.time() + g.lifespan

from .mediaws import *


class imaple(MediaWs):
    _root_url = "https://imaple.co"

    def __init__(self, apiurl: str) -> None:
        super().__init__(apiurl=apiurl)

    def cats(self) -> list:
        self._cats_body = {
            "url": "{}".format(self._root_url),
            "items": {
                "cat": {"xpath": "/html/body/header/div/div/ul[1]/li[1]/div/ul/li/a", "attr": "text", "unique": False, "ignnone": False},
                "url": {"xpath": "/html/body/header/div/div/ul[1]/li[1]/div/ul/li/a", "attr": "href", "unique": False, "ignnone": False},
            }
        }
        return super().cats()

    def scats(self, cat: str) -> list:
        self._scats_body = {
            "url": "{}/type/{}.html".format(self._root_url, cat),
            "items": {
                "url": {"xpath": "/html/body/div[1]/div/div[1]/div/div[2]/div/ul[1]/li/a", "attr": "href", "unique": False, "match": r"/show/(.*?)\.html"},
            }
        }
        return super().scats(cat=cat)

    def videos_list(self, scat: str) -> list:
        self._videos_body = {
            "url": "{}/type/{}/by/time.html".format(self._root_url, scat),
            "items": {
                # "name": {"xpath": "/html/body/div[1]/div/div[2]/div/div/ul/li/div/a", "attr": "title"},
                # "img": {"xpath": "/html/body/div[1]/div/div[2]/div/div/ul/li/div/a", "attr": "data-original"},
                "id": {"xpath": "/html/body/div[1]/div/div[2]/div/div/ul/li/div/a", "attr": "href", "re": {"^/vod/": "", ".html$": ""}},
            }
        }
        return super().videos_list(scat=scat)

    def videos_info(self, vid: str) -> list:
        self._videos_info_body = {
            "url": "{}/vod/{}.html".format(self._root_url, vid),
            "items": {
                "scat": {"xpath": "/html/body/div[2]/div/div/div/div/div/div[2]/p[2]/a[1]", "attr": "text"},
                "title": {"xpath": "/html/body/div[2]/div/div/div/div/div/div[2]/h1", "attr": "text"},
                "region": {"xpath": "/html/body/div[2]/div/div/div/div/div/div[2]/p[2]/a[2]", "attr": "text"},
                "year": {"xpath": "/html/body/div[2]/div/div/div/div/div/div[2]/p[2]/a[3]", "attr": "text"},
                "actors": {"xpath": "/html/body/div[2]/div/div/div/div/div/div[2]/p[3]/a", "attr": "text", "multi": True},
                "directors": {"xpath": "/html/body/div[2]/div/div/div/div/div/div[2]/p[4]/a", "attr": "text", "multi": True},
                "img": {"xpath": "/html/body/div[2]/div/div/div/div/div/div[1]/a/img", "attr": "data-original"},
                "update": {"xpath": "/html/body/div[2]/div/div/div/div/div/div[2]/p[6]/span[2]", "attr": "text", "re": {"^(.*)/": ""}, "dateformat": "%Y-%m-%d %H:%M:%S"},
                "url": {"xpath": "/html/body/div[3]/div/div[1]/div/div[2]/div/ul/li/a", "attr": "href", "multi": True},
            }
        }
        return super().videos_info(vid=vid)

    def streams(self, vid: str, st: int = 1, ep: int = 1) -> list:
        self._streams_body = {
            "url": "{}/play/{}-{}-{}.html".format(self._root_url, vid, st, ep),
            "items": {
                "url": {"xpath": "/html/body/div[2]/div/div/div/div[1]/div/div[2]/script[1]", "attr": "json", "re": {"^var\s+?\w+?=": "", ";$": ""}, "key": "url"},
                "url_next": {"xpath": "/html/body/div[2]/div/div/div/div[1]/div/div[2]/script[1]", "attr": "json", "re": {"^var\s+?\w+?=": "", ";$": ""}, "key": "url_next"},
            }
        }
        return super().streams(vid=vid, st=st, ep=ep)

    def videos(self, cat: str = None, scat: str = None, limit: int = 500, incl_info: bool = True) -> list:
        return super().videos(cat=cat, scat=scat, limit=limit, incl_info=True)

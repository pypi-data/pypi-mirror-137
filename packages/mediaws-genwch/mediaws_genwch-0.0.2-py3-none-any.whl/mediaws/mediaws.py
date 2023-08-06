from abc import ABC


class MediaWs(ABC):
    _root_url = "https://imaple.co"
    _cats_body = None
    _scats_body = None
    _videos_body = None
    _videos_info_body = None
    _streams_body = None

    def __init__(self, apiurl: str) -> None:
        self._apiurl = apiurl
        pass

    def _apiws(self, body: dict) -> list:
        import requests
        _req = requests.get(self._apiurl, json=body)
        if _req.status_code == 200:
            _req.encoding = 'utf-8'
            _j = _req.json()
            if _j.get("code", None) == 200:
                return _j.get("data", [])
        return []

    def _dl2ld(self, dl: dict) -> dict:
        return [dict(zip(dl, t)) for t in zip(*dl.values())]

    def _re_extract(self, pattern: str, value: str, index: int = 1) -> str:
        import re
        try:
            return re.search(pattern, value).group(index)
        except:
            return None

    def cats(self) -> list:
        _cats_body = {
            "url": "{}".format(self._root_url),
            "items": {
                "url": {"xpath": "/html/body/header/div/div/ul[1]/li[1]/div/ul/li/a", "attr": "href", "match": r"/type/(.*?)\.html"},
            }
        } if self._cats_body is None else self._cats_body
        _items = self._apiws(_cats_body)
        if len(_items) <= 0:
            return []
        _rtn = []
        for _v in _items[0].get("url", []):
            _id = self._re_extract(
                pattern=r"/type/(.*?)\.html", value=_v)
            if _id == None:
                continue
            _rtn.append({"id": _id})
        return _rtn

    def scats(self, cat: str) -> list:
        _scats_body = {
            "url": "{}/type/{}.html".format(self._root_url, cat),
            "items": {
                "url": {"xpath": "/html/body/div[1]/div/div[1]/div/div[2]/div/ul[1]/li/a", "attr": "href", "match": r"/show/(.*?)\.html"},
            }
        } if self._scats_body is None else self._scats_body
        _items = self._apiws(_scats_body)
        if len(_items) <= 0:
            return []
        _items = self._dl2ld(_items[0])
        _rtn = []
        for _v in _items:
            _id = self._re_extract(
                pattern=r"/show/(.*?)\.html", value=_v.get("url"))
            if _id == None:
                continue
            _rtn.append({"id": _id})
        return _rtn

    def videos_list(self, scat: str) -> list:
        _videos_body = {
            "url": "{}/type/{}.html".format(self._root_url, scat),
            "items": {
                "name": {"xpath": "/html/body/div[1]/div/div[2]/div/div/ul/li/div/a", "attr": "title"},
                "img": {"xpath": "/html/body/div[1]/div/div[2]/div/div/ul/li/div/a", "attr": "data-original"},
                "id": {"xpath": "/html/body/div[1]/div/div[2]/div/div/ul/li/div/a", "attr": "href", "re": {"^/vod/": "", ".html$": ""}},
            }
        } if self._videos_body is None else self._videos_body
        _items = self._apiws(_videos_body)
        if len(_items) <= 0:
            return []
        _items = self._dl2ld(_items[0])
        return _items

    def _handle_datetime(self, value: dict, body: dict) -> dict:
        from datetime import datetime
        for _k, _v in value.items():
            _dateformat = body.get("items", {}).get(
                _k, {}).get("dateformat", None)
            if _dateformat == None:
                continue
            value.update({_k: datetime.strptime(_v, _dateformat)})
        return value

    def videos_info(self, vid: str) -> dict:
        _videos_info_body = {
            "url": "{}/vod/{}.html".format(self._root_url, vid),
            "items": {
                "scat": {"xpath": "/html/body/div[2]/div/div/div/div/div/div[2]/p[2]/a[1]", "attr": "text"},
                "region": {"xpath": "/html/body/div[2]/div/div/div/div/div/div[2]/p[2]/a[2]", "attr": "text"},
                "year": {"xpath": "/html/body/div[2]/div/div/div/div/div/div[2]/p[2]/a[3]", "attr": "text"},
                "actors": {"xpath": "/html/body/div[2]/div/div/div/div/div/div[2]/p[3]/a", "attr": "text", "multi": True},
                "directors": {"xpath": "/html/body/div[2]/div/div/div/div/div/div[2]/p[4]/a", "attr": "text", "multi": True},
                "update": {"xpath": "/html/body/div[2]/div/div/div/div/div/div[2]/p[6]/span[2]", "attr": "text", "re": {"^(.*)/": ""}, "dateformat": "%Y-%m-%d %H:%M:%S"},
                "url": {"xpath": "/html/body/div[3]/div/div[1]/div/div[2]/div/ul/li/a", "attr": "href", "multi": True},
            }
        } if self._videos_info_body is None else self._videos_info_body
        _items = self._apiws(_videos_info_body)
        if len(_items) <= 0:
            return {}
        _items = _items[0]
        _info = _items
        _eps = {"url": _items.get("url", [])}
        _eps = self._dl2ld(_eps)
        _info.pop("url")
        _max_st = 0
        _max_ep = 0
        for _e in _eps:
            _url = _e.get("url", "")
            _st = self._re_extract(
                pattern=r"^/play/\d+-(\d+?)-(\d+?).html$", value=_url, index=1)
            _ep = self._re_extract(
                pattern=r"^/play/\d+-(\d+?)-(\d+?).html$", value=_url, index=2)
            _max_st = max(_max_st, int(_st))
            _max_ep = max(_max_ep, int(_ep))
        _info.update({"st": _max_st, "ep": _max_ep})
        _info = self._handle_datetime(_info, _videos_info_body)
        return _info

    def streams(self, vid: str, st: int = 1, ep: int = 1) -> dict:
        _streams_body = {
            "url": "{}/play/{}-{}-{}.html".format(self._root_url, vid, st, ep),
            "items": {
                "url": {"xpath": "/html/body/div[2]/div/div/div/div[1]/div/div[2]/script[1]", "attr": "json", "re": {"^var\s+?\w+?=": "", ";$": ""}, "key": "url"},
                "url_next": {"xpath": "/html/body/div[2]/div/div/div/div[1]/div/div[2]/script[1]", "attr": "json", "re": {"^var\s+?\w+?=": "", ";$": ""}, "key": "url_next"},
            }
        } if self._streams_body is None else self._streams_body
        _items = self._apiws(_streams_body)
        if len(_items) <= 0:
            return {}
        _rtn = {_k: _v for _k, _v in _items[0].items() if _v != ""}
        return _rtn

    def videos(self, cat: str = None, scat: str = None, limit: int = 500, incl_info: bool = True) -> list:
        _rtn = []
        for _c in self.cats():
            if cat != None and _c.get("id") != cat:
                continue
            for _s in self.scats(_c.get("id")):
                if _c.get("id") == _s.get("id"):
                    continue
                if scat != None and _s.get("id") != scat:
                    continue
                for _v in self.videos_list(_s.get("id")):
                    _v.update({"cat_id": _c.get("id"),
                              "scat_id": _s.get("id")})
                    if incl_info:
                        _info = self.videos_info(_v.get("id"))
                        for _ik, _iv in _info.items():
                            _v.update({_ik: _iv})
                    _rtn.append(_v)
                if scat != None:
                    return _rtn
            if len(_rtn) >= limit and limit > 0:
                break
        return _rtn

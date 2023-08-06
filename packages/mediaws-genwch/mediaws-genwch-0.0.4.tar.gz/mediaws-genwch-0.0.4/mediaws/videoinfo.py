from abc import ABC


class videoinfo(ABC):
    def __init__(self) -> None:
        pass

    def clean_title(self, title: str) -> tuple:
        import re
        if title is None or title == "":
            return None, None
        _extracts = [("\[", "\]"), ("【", "】"), ("（", "）"), ("\(", "\)")]
        _tail = None
        for _e in _extracts:
            _grp = re.match(f"^(.*){_e[0]}(.*){_e[1]}$", title)
            if _grp:
                _tail = _grp.group(2)
                title = _grp.group(1)
                break
        if _tail is None:
            _tails = ["未刪減版", "國語", "粵語", "美版", "英語", "韓語", "日語", "韓版", "日版"]
            for _t in _tails:
                _grp = re.match(f"\w*({_t})$", title)
                if _grp:
                    _tail = _t
                    title = re.sub(f"{_t}$", "", title)
                    break
        return title.strip(), _tail.strip() if _tail else None

    def conv_region(self, region: str) -> list:
        import re
        _regions = region.split(",")
        _conv = [("中國香港", "hk"), ("香港", "hk"), ("中國台灣", "tw"), ("台灣", "tw"), ("中國大陸", "cn"), ("中國", "cn"), ("大陸", "cn"),
                 ("美國", "us"), ("英國", "uk"), ("法國", "fr"), ("德國", "de"), ("日本", "jp"), ("韓國", "kr"), ("西班牙", "es")]
        _tar_conv = [_t for _f, _t in _conv]
        _rtn = []
        for _r in _regions:
            for _f, _t in _conv:
                _r = re.sub(_f, _t, _r)
            _r = "ot" if _r not in _tar_conv else _r
            _rtn.append(_r)
        return _rtn

    def is_chinese(self, regions: list) -> bool:
        for _r in regions:
            if _r in ["cn", "hk", "tw"]:
                return True
        return False

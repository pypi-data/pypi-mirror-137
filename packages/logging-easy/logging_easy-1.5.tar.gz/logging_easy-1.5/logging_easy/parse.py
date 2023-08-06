def parse_log(what, tab, start=True):
    res = ""
    if dir(what) is not None:
        if start:
            res += (" " * (tab - 2))
        res += (str(what)) + " {\n"
        for attr in dir(what):
            if attr.startswith("__") or callable(getattr(what, attr)):
                continue
            if isinstance(getattr(what, attr), list):
                res += (" " * tab) + attr + ": "
                res += "[\n"
                for item in getattr(what, attr):
                    res += parse_log(item, tab + 4)
                res += (" " * tab) + "],\n"
            elif isinstance(getattr(what, attr), str) or isinstance(getattr(what, attr), int) or isinstance(
                    getattr(what, attr), float):
                if isinstance(getattr(what, attr), str):
                    res += ((" " * tab) + f"{attr}: \"{getattr(what, attr)}\",\n")
                res += ((" " * tab) + f"{attr}: {getattr(what, attr)},\n")
            else:
                res += ((" " * tab) + f"{attr}: {parse_log(getattr(what, attr), tab + 2, False)}")
        res += (" " * (tab - 2)) + "},\n"

        return res
    else:
        return what
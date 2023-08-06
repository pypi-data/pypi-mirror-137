from .parse import parse_log


def log(what, tab=2):
    print(parse_log(what, tab))

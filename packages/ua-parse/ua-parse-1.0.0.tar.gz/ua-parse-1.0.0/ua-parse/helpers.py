import inspect
import itertools
import re
from typing import Optional

from ua_parse.constants import UNKNOWN, DEFAULT_FLAGS


def is_str(value):
    return isinstance(value, str)


def is_array(value):
    return isinstance(value, list)


def is_func(value):
    return inspect.isfunction(value)


def lowerize(value: str):
    return value.lower()


def trim(value: str, length: Optional[int] = 0):
    if not (is_str(value)):
        return

    value = re.sub(r"^\s\s*", '', value)
    value = re.sub(r"\s\s *$", '', value)

    return value[:length] if length else value


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"

    args = [iter(iterable)] * n
    return list(itertools.zip_longest(*args, fillvalue=fillvalue))


def str_mapper(string: str, map: dict):
    for key, val in map.items():
        values = val if is_array(val) else [val]

        for value in values:
            if lowerize(value) in lowerize(string):
                if key == UNKNOWN:
                    return None

                return key

    return string


def proccess_prop(prop, group) -> tuple[str, str]:
    """
    Returns:
        Tuple with (key, value)
    """
    if not is_array(prop):
        return (prop, group or None)

    key = prop[0]
    value = None

    if len(prop) == 2:
        if is_func(prop[1]):
            value = prop[1](group)
        else:
            value = prop[1]
    elif not group:
        pass
    elif len(prop) == 3:
        if is_func(prop[1]):
            value = prop[1](group, prop[2])
        else:
            value = re.sub(prop[1], prop[2], group)
    elif len(prop) == 4:
        value = prop[3](re.sub(prop[1], prop[2], group))

    return (key, value)


def rgx_mapper(ua: str, arrays: list):
    res = {}

    if not ua:
        return res

    for (regexs, props) in grouper(arrays, 2):
        for regex in regexs:
            match = re.search(regex, ua, flags=DEFAULT_FLAGS)

            if match:
                groups = match.groups()
                for prop, group in itertools.zip_longest(props, groups):
                    key, value = proccess_prop(prop, group)
                    res[key] = value

                return res

    return res

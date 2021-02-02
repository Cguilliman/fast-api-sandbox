import re
from typing import *
from .config import settings
from collections import defaultdict

# Core functional
VALUE_GETTERS = {
    lambda values: settings.VALUE_SPLITER in values: lambda values: values.split(settings.VALUE_SPLITER),
    lambda values: settings.RANGE_SPLITER in values: lambda values: values.split(settings.RANGE_SPLITER),
}
KEY_VALUE_SCHEMA = "(?P<var>\w+){}(?P<values>[^{}]+)".format(settings.KEY_VALUE_SPLITER, settings.FILTER_SPLITER)
KEY_VALUE_PATTERN = re.compile(KEY_VALUE_SCHEMA)


def is_empty(value, empty: Iterable = settings.EMPTY_VALUES) -> bool:
    return any(value == item for item in empty)


def check_value(value, empty: Iterable = settings.EMPTY_VALUES) -> Any:
    return None if is_empty(value, empty) else value


def convert_value(value, values_map: Dict = settings.STRING_VALUES_MAP):
    return values_map[value] if value in values_map else value


def build_values(values):
    for value in values:
        value = convert_value(value)
        if not check_value(value):
            continue
        yield value


def _parse_values(values: str):
    for excretion, getter in VALUE_GETTERS.items():
        if excretion(values):
            return list(build_values(getter(values)))
    return list(build_values([values]))


def parse(filters: str):
    parsed_filters = defaultdict(list)

    pattern = KEY_VALUE_PATTERN
    for _filter in filters.split(settings.FILTER_SPLITER):
        match = pattern.match(_filter)
        if not match:
            continue
        var = match.group("var")
        values = _parse_values(match.group("values"))
        if not is_empty(values):
            parsed_filters[var].extend(values)
    return parsed_filters

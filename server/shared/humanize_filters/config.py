from dataclasses import dataclass


@dataclass
class Settings:
    VALUE_SPLITER=","
    RANGE_SPLITER="~"
    FILTER_SPLITER=";"
    KEY_VALUE_SPLITER="="
    EMPTY_VALUES=("undefined", "null", "", None, [], (), {})
    STRING_VALUES_MAP={
        'undefined': None,
        'null': None,
        'None': None,
        'True': True,
        'true': True,
        'False': False,
        'false': False,
    }
    FILTER_URL_VAR="filters"
    FILTERS_LABEL="filters"


settings = Settings()

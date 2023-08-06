"""Provides enums required for Nawah Fremework and apps"""

from enum import Enum, auto


class Event(Enum):
    """Identifies events in calls that can be skipped"""

    ARGS = auto()
    VALIDATE = auto()
    PERM = auto()
    CACHE = auto()
    PRE = auto()
    ON = auto()
    EXTN = auto()
    SOFT = auto()
    DIFF = auto()
    SYS_DOCS = auto()


class DELETE_STRATEGY(Enum):
    """Identifies strategies of delete calls"""

    SOFT_SKIP_SYS = auto()
    SOFT_SYS = auto()
    FORCE_SKIP_SYS = auto()
    FORCE_SYS = auto()


class LOCALE_STRATEGY(Enum):
    """Identifies strategies of values for attrs of Attr Type LOCALE"""

    DUPLICATE = auto()
    NONE_VALUE = auto()


class NAWAH_VALUES(Enum):
    """Identifies values to be used internally to pass secure values"""

    NONE_VALUE = auto()
    ALLOW_MOD = auto()

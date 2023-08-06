import logging
from enum import IntEnum, Enum
from typing import List, Dict, Tuple

from .cached_settings import CachedSettings

logger = logging.getLogger(__file__)


class Scope(IntEnum):
    VENDOR = 1
    CLIENT = 2
    GROUP = 3
    DEVICE = 4
    USER = 5


class ScopeIcons(Enum):
    VENDOR = "box"
    CLIENT = "person-badge"
    GROUP = "people-fill"
    DEVICE = "display"
    USER = "person-fill"


class SettingsRegistry:
    """A in-memory storage where settings namespaces/keys/scopes are registered at application start
    and can be checked against for existence.

    Every available setting *must* be registered before usage.
    """

    _registered_keys = {}  # type: Dict[Tuple[str, str, Scope],type]

    def __init__(self):
        raise NotImplementedError(
            f"{self.__class__.__name__} is not meant to be instantiated."
        )

    @classmethod
    def register(cls, namespace, key, allowed_scopes: List["Scope"], key_type=str):
        """Registers a settings variable in a global list.

        This makes sure that settings variables read in from e.g. .toml files can only be accepted if they
        match existing, already registered settings.
        """

        # VENDOR scope is always allowed
        if not Scope.VENDOR in allowed_scopes:
            allowed_scopes.append(Scope.VENDOR)

        for scope in allowed_scopes:
            t = (namespace, key, scope)
            # can't register same key with different type
            if t in cls._registered_keys.keys():
                logger.warning(
                    f"Key {namespace}.{key} with scope '{scope.name}' was already registered!"
                )
            else:
                cls._registered_keys[t] = key_type

    @classmethod
    def exists(cls, namespace, key, scope) -> bool:
        """:returns True if given namespace.key/scope is registered."""

        # return (namespace, key, scope) in cls._registered_keys
        return (namespace, key, scope) in cls._registered_keys.keys()

    @classmethod
    def scopes(cls, namespace: str, key: str) -> set:
        scopes = set()
        for s in cls._registered_keys.keys():
            if s[0] == namespace and s[1] == key:
                scopes.add(s[2])
        return scopes

    @classmethod
    def all_dct(cls) -> Dict[str, Dict[str, str]]:
        _all = {}
        for namespace, key, scope in cls._registered_keys.keys():
            if not namespace in _all:
                _all[namespace] = {}
            if not key in _all[namespace]:
                _all[namespace][key] = {}

            _all[namespace][key][scope] = ""
        return _all

    @classmethod
    def all(cls):
        """:returns a dict of all registered settings keys"""
        for setting, key_type in cls._registered_keys.items():
            yield setting + (key_type,)

from __future__ import annotations

import json
from json import JSONDecodeError
from threading import Lock
from typing import Any, Optional

from .constants import CONFIG_FILENAME
from .exceptions import AuthenticationError


class ConfigMeta(type):
    _instances = {}  # type: ignore
    _lock: Lock = Lock()  # type: ignore

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
            return cls._instances[cls]


class Config(metaclass=ConfigMeta):
    """Config helper class."""

    config_properties: list = [
        'api_key'
    ]

    def __init__(self):
        """Constructs Config object."""
        self._api_key: Optional[str] = None

    @property
    def api_key(self) -> Optional[str]:
        """API key property of the Config object.

        Returns:
            str: API key.
        """
        if self._api_key:
            return self._api_key
        else:
            try:
                with open(CONFIG_FILENAME) as config_read:
                    self._api_key = json.load(config_read)['api_key']
                    return self._api_key
            except FileNotFoundError:
                raise AuthenticationError()
            except JSONDecodeError:
                raise

    @api_key.setter
    def api_key(self, value):
        self._api_key = value

    def save(self):
        """Saves configuration to the JSON config file."""
        with open(CONFIG_FILENAME, 'w') as config_write:
            # TODO FUTURE: select only specific keys
            config_load = {k: getattr(self, k)
                           for k in Config.config_properties}
            json.dump(config_load, config_write)

    def __str__(self) -> str:
        """Returns structured configuration information."""
        return str(self.__dict__)

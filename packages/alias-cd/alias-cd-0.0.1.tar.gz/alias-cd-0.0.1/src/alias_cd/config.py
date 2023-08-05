"""This module contains the logic to interact with the alias_cd configuration file."""

from dataclasses import dataclass
from typing import Dict
import os

import yaml


ALIAS_KEY = "_alias"
DEFAULT_CONFIG_PATH = os.path.join(
    os.path.expanduser("~"), ".config", "alias_cd", "config.yaml"
)


@dataclass
class Config:
    """This config contains the alias_cd configuration information."""

    aliases: Dict[str, str]

    def get_directory(self, alias: str) -> str:
        """Return the directory for a given alias."""

        return os.path.expanduser(self.aliases[alias])

    def has_aias(self, alias: str) -> bool:
        """Check if the supplied alias is contained in the config."""

        return alias in self.aliases


def load_config(config_path: str = None) -> Config:
    """Parse the configuration file from the supplied config_path."""

    if config_path is None:
        config_path = DEFAULT_CONFIG_PATH

    if not os.path.exists(config_path):
        raise ValueError(f"No config file found at {config_path}")

    with open(config_path, "r") as stream:
        config_yaml = _load_yaml(stream)

    return _get_config(config_yaml)


def _get_config(config_yaml: Dict) -> Config:

    return Config(aliases=_get_aliases(config_yaml))


def _load_yaml(data):
    return yaml.safe_load(data)


def _get_aliases(config_yaml: Dict, base_path="") -> Dict[str, str]:
    """Depth first search for aliases."""

    aliases = {}

    if ALIAS_KEY in config_yaml:
        aliases[config_yaml["_alias"]] = base_path

    for key, value in config_yaml.items():
        if key != ALIAS_KEY:
            als = _get_aliases(value, base_path=os.path.join(base_path, key))
            if als:
                aliases.update(als)

    return aliases

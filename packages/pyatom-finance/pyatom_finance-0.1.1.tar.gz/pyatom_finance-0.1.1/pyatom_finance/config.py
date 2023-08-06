"""PyDantic global settings and configuration"""
import os

from pathlib import Path
from pydantic import BaseSettings

import toml


SETTINGS = None


class Settings(BaseSettings):
    """Base settings used throughout PyAtom_Finance"""

    atom_url: str = "https://atom.finance/graphql"
    atom_signin_url: str = "https://atom.finance/session/signin"
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    jinja2_templates: str = os.path.join(base_dir, "pyatom_finance/templates")
    username: str = os.environ.get("ATOM_USERNAME", "")
    password: str = os.environ.get("ATOM_PASSWORD", "")


def load(config_file_name="pyproject.toml"):
    """PyDantic load function"""
    global SETTINGS
    if os.path.exists(config_file_name):
        config_string = Path(config_file_name).read_text()
        config_tmp = toml.loads(config_string)

        if "tool" in config_tmp and "atom_finance" in config_tmp.get("tool", {}):
            SETTINGS = Settings(**config_tmp["tool"]["atom_finance"])
            return

    SETTINGS = Settings()

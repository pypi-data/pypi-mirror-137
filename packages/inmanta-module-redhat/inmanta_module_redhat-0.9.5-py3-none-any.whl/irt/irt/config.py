"""
    :copyright: 2021 Inmanta
    :contact: code@inmanta.com

    This file defines the schema of config.toml

"""
from typing import Dict

import pydantic

import irt.module_sources


class Config(pydantic.BaseModel):

    module_sources: Dict[str, irt.module_sources.ModuleSourceConfig]

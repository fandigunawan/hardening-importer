"""Hardening Importer - Import IronBank Hardening Manifests for builds.

This module is for encapsulating the schema of the manifest and validating it.
"""

import yaml
from pydantic import BaseModel, Field
from typing import Dict, List, Optional

from .common import StrEnum


class ResourceValidationType(StrEnum):
    """The type of validations that are supported."""

    SHA256 = 'sha256'
    SHA512 = 'sha512'


class HardeningResourceValidation(BaseModel):
    """A pythonic API object for resource validation fields."""

    type: ResourceValidationType
    value: str


class HardeningResource(BaseModel):
    """A pythonic API object for resources listed in hardening manifests."""

    filename: str
    url: str
    validation: HardeningResourceValidation


class HardeningManifestMaintainer(BaseModel):
    """A pythonic API object for hardening manifest maintainer entries."""

    name: str
    email: str
    username: str
    cht_member: Optional[bool]


class HardeningManifest(BaseModel):
    """A pythonic API object for interacting with a hardening manifest."""

    apiVersion: str = Field(default='v1')
    name: str
    tags: List[str] = Field(default=['latest'])
    args: Optional[Dict[str, str]]
    labels: Optional[Dict[str, str]]
    resources: Optional[List[HardeningResource]]
    maintainers: List[HardeningManifestMaintainer]

    @classmethod
    def from_yaml(cls, yaml_file: str) -> 'HardeningManifest':
        """Instantiate a HardeningManifest from a yaml file path."""
        with open(yaml_file) as f:
            manifest = yaml.safe_load(f)
        return cls.parse_obj(manifest)

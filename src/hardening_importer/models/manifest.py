"""Hardening Importer - Import IronBank Hardening Manifests for builds.

This module is for encapsulating the schema of the manifest and validating it.
"""

import hashlib
import os
from pydantic import BaseModel, Field
import requests
from typing import Dict, List, Optional
import yaml

from .common import StrEnum
from ..util import get_logger
from ..exceptions import ChecksumValidationError


class ResourceValidationType(StrEnum):
    """The type of validations that are supported."""

    SHA256 = 'sha256'
    SHA512 = 'sha512'


class HardeningResourceValidation(BaseModel):
    """A pythonic API object for resource validation fields."""

    type: ResourceValidationType
    value: str

    def validate_hash(self, digest: str = None) -> bool:
        """Validate that the provided digest matches the expected value."""
        logger = get_logger()
        if self.value.lower() == digest.lower():
            logger.info(f'Hash of {digest} matches {self.value}')
            return True
        return False


class HardeningResource(BaseModel):
    """A pythonic API object for resources listed in hardening manifests."""

    filename: str
    url: str
    validation: HardeningResourceValidation

    def download_and_validate(self, output: str = None) -> None:
        """Download from the URL, validate the hash, write the file."""
        logger = get_logger()
        # Download from URL
        logger.info(f'Downloading from {self.url}')
        data = requests.get(self.url).content
        # Grab the right validation algorithm
        logger.debug(f'Validating with hash of type {self.validation.type}')
        hash_algo = getattr(hashlib, self.validation.type)
        # Initialize the hasher
        data_hash = hash_algo()
        # Hash the data
        data_hash.update(data)
        logger.info(f'Downloaded file with hash {data_hash.hexdigest()}')
        # Compare the digests
        if self.validation.validate_hash(data_hash.hexdigest()):
            # Write the file
            if output is not None:
                output = os.path.realpath(output)
                os.makedirs(output, exist_ok=True)
                outfile = os.path.join(output, self.filename)
            else:
                output = os.getcwd()
                outfile = self.filename
            logger.info(f'Writing file to {self.filename} in {output}')
            with open(outfile, 'wb') as f:
                f.write(data)
        else:
            raise ChecksumValidationError((
                f'The hash for {self.filename} did not match the expected '
                f'value of {self.validation.value}'
            ))


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

    def download_resources(self, output: str = None) -> None:
        """Download all subordinate resources."""
        logger = get_logger()
        logger.info(f'Downloading resources for {self.name}')
        for resource in self.resources:
            resource.download_and_validate(output=output)

    def _kaniko_args(self,
                     context_dir: str = None,
                     dockerfile: str = 'Dockerfile',
                     registry: str = 'quay.io') -> List[str]:
        """Build a command line argument set for Kaniko."""
        args = ['--context', context_dir]
        args += ['--dockerfile', os.path.join(context_dir, dockerfile)]
        for tag in self.tags:
            args += ['--destination', f'{registry}/{self.name}:{tag}']
        return args

    def build_args(self,
                   context_dir: str = None,
                   dockerfile: str = 'Dockerfile',
                   registry: str = 'quay.io',
                   executor: str = 'kaniko') -> List[str]:
        """Build a command line argument set for the executor."""
        if executor == 'kaniko':
            return self._kaniko_args(context_dir=context_dir,
                                     dockerfile=dockerfile, registry=registry)
        else:
            raise RuntimeError(f'Unable to prepare build args for {executor}')

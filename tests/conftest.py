"""Hardening Importer - Import IronBank Hardening Manifests for builds.

This module contains test configuration for pytest.
"""

import os
import pytest
import shutil
import tempfile

example_dir = os.path.realpath(os.path.join(
    os.path.dirname(__file__), '../examples'
))

VALID_MANIFESTS = [
    f'{example_dir}/example_hardening_manifest.yaml'
]
INVALID_MANIFESTS = [
    f'{example_dir}/example_invalid_hardening_manifest_bad_args.yaml',
    f'{example_dir}/example_invalid_hardening_manifest_bad_hash.yaml',
    f'{example_dir}/example_invalid_hardening_manifest_bad_resources.yaml'
]


@pytest.fixture()
def new_folder() -> str:
    """Change directory into a new temp folder.

    Yields the folder name, cleaning up the directory after test runs complete.
    """
    folder = tempfile.mkdtemp()
    original_folder = os.getcwd()
    os.chdir(folder)
    yield folder
    os.chdir(original_folder)
    shutil.rmtree(folder)

# Hardening Importer

Ingest Iron Bank hardening manifests, produce a build environment.

## Prerequisites

You must configure a GitLab personal access token to use HTTP basic auth. Please see the user profile page for creating these tokens [here](https://gitlab.jharmison.com/-/profile/personal_access_tokens). You will be required to input this token to authenticate.

## Usage

```sh
# When prompted for your username, enter `__token__`
# When prompted for your password, enter your personal GitLab access token
pip3 install --user hardening-importer --extra-index-url https://gitlab.jharmison.com/api/v4/projects/4/packages/pypi/simple
hardening import .
```

## Details

Parses the hardening_manifest.yaml file located in the provided directory and downloads the files listed in the `resources` list. Validate their sums, as listed. Generates a commandline to use with [Kaniko](https://github.com/GoogleContainerTools/kaniko) for building the image listed and outputting it to stdout. This can be integrated with GitLab by following their instructions for using Kaniko in your image builds, accessible [here](https://docs.gitlab.com/ee/ci/docker/using_kaniko.html)

## Advanced usage

You can run `hardening-import --help` to get more detailed usage instructions.

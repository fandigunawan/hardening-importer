# Hardening Importer

Ingest Iron Bank hardening manifests, produce a build environment.

## Usage

```sh
pip3 install --user git+https://gitlab.jharmison.com/dco/hardening-importer.git@main
hardening-import .
```

## Details

Parses the hardening_manifest.yaml file located in the provided directory and downloads the files listed in the `resources` list. Validate their sums, as listed. Generates a commandline to use with [Kaniko](https://github.com/GoogleContainerTools/kaniko) for building the image listed and outputting it to stdout. This can be integrated with GitLab by following their instructions for using Kaniko in your image builds, accessible [here](https://docs.gitlab.com/ee/ci/docker/using_kaniko.html)

## Advanced usage

You can run `hardening-import --help` to get more detailed usage instructions.

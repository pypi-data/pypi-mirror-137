# `pypi-name-squatter`

This repository contains the minimal amount of code to build a Python package,
whose purpose is to be uploaded onto [PyPI](https://pypi.org/) in the name of
[name squatting](https://github.com/pypa/warehouse/issues/4004). The purpose of
this is to prevent
[dependency confusion](https://medium.com/@alex.birsan/dependency-confusion-4a5d60fec610)
attacks.

## Steps

1. Modify the package name in `pyproject.toml` from `clsa_test` to the new
   project name.

1. Modify the directory named `clsa_test` to the new project name.

1. Publish to [PyPI](https://pypi.org/):

   ```bash
   ./publish
   ```

   This script will automatically commit the above changes before publishing,
   and then roll them back by resetting the repository.

1. Update the table below.

## Registered packages:

| Date       | Package                                                      |
| ---------- | ------------------------------------------------------------ |
| 2022-01-26 | [`clsa_test`](https://pypi.org/project/clsa_test/)           |
| 2022-01-26 | [`clsa_pypi`](https://pypi.org/project/clsa_pypi/)           |
| 2022-01-26 | [`clsa_utilities`](https://pypi.org/project/clsa_utilities/) |
| 2022-01-26 | [`clsa_axioma`](https://pypi.org/project/clsa_axioma/)       |
| 2022-01-26 | [`clsa_refinitiv`](https://pypi.org/project/clsa_refinitiv/) |
| 2022-01-27 | [`clsa_wind`](https://pypi.org/project/clsa_wind/)           |
| 2022-01-27 | [`clsa_stat_arb`](https://pypi.org/project/clsa_stat_arb/)   |
| 2022-01-28 | [`clsa_oracle`](https://pypi.org/project/clsa_oracle/)       |

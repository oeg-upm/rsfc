# Research Software Fairness Checks (RSFC)

A command line interface to automatically evaluate the quality of a Github or Gitlab repository.

**Authors**: Daniel Garijo, Andrés Montero


## Features

Given a repository URL, RSFC will perform a series of checks based on a list of research software quality indicators (RSQI). The RSQIs currently covered by the package are:

- software_has_license
- software_has_citation
- has_releases
- repository_workflows
- version_control_use
- requirements_specified
- software_documentation
- persistent_and_unique_identifier
- descriptive_metadata

For more information about these RSQIs, you can check https://github.com/EVERSE-ResearchSoftware/indicators. We have plans to implement all of the RSQIs available in that repository.


## Requirements

Python 3.10.8 or higher

Dependencies are available in the requirements.txt file located in the root of the repository

## Install from Github

To install the package, first clone the repository in your machine

```
git clone https://github.com/oeg-upm/rsfc.git
```

Go to the project's root directory

```
cd rsfc
```

And then run in that directory

```
pip install .
```

## Usage

After installation, you can use the package by running

```
rsfc <repo_url>
```
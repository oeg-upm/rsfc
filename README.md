[![DOI](https://zenodo.org/badge/993095977.svg)](https://doi.org/10.5281/zenodo.16531481) [![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)


# Research Software FAIRness Checks (RSFC)

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
- software_tests
- archived_in_software_heritage
- versioning_standards_use
- support_issue_tracking

For more information about these RSQIs, you can check https://github.com/EVERSE-ResearchSoftware/indicators. We have plans to implement all of the RSQIs available in that repository.


## Available tests

RSFC can perform the following tests:

- RSFC-01-1: There is an identifier and it resolves
- RSFC-01-2: There is an identifier in the metadata files
- RSFC-01-3: There is an identifier and it follows a common schema
- RSFC-03-1: The software has releases
- RSFC-03-2: Releases have version and identifier
- RSFC-03-3: Release versions follow SemVer or CalVer
- RSFC-03-4: Release identifiers follow the same scheme
- RSFC-03-5: Last release version corresponds to version in package file
- RSFC-03-6: There is a version number stated in metadata files
- RSFC-04-1: Metadata files exist
- RSFC-04-2: There is a README file
- RSFC-04-3: Title and description are declared
- RSFC-04-4: There is descriptive metadata
- RSFC-04-5: There is a codemeta file
- RSFC-05-1: There is a repostatus badge in the README file
- RSFC-05-2: Contact and support metadata exists
- RSFC-05-3: Software documentation exists
- RSFC-06-1: Authors are declared
- RSFC-06-2: Contributors are declared
- RSFC-06-3: Authors have an ORCID assigned
- RSFC-06-4: Authors have their role stated
- RSFC-07-1: There is an identifier in README or CITATION
- RSFC-07-2: Software identifier resolves and links back to software
- RSFC-08-1: Metadata record is found in SWHeritage or Zenodo
- RSFC-09-1: Repository is from Github or Gitlab
- RSFC-12-1: There is an article citation or reference publication
- RSFC-13-1: Dependencies are declared
- RSFC-13-2: There are installation instructions
- RSFC-13-3: Dependencies have version numbers
- RSFC-13-4: Dependencies are in a machine-readable format
- RSFC-14-1: Tests are provided
- RSFC-14-2: There are actions to automate tests
- RSFC-15-1: There is a license
- RSFC-15-2: License is in SPDX format
- RSFC-15-3: License information is provided
- RSFC-16-1: License is referenced in metadata files
- RSFC-17-1: The repository has an 'active' status
- RSFC-17-2: Repository has a commit history
- RSFC-17-3: Commits are linked to issues
- RSFC-18-1: There are citations
- RSFC-19-1: Repository has continuous integration workflows
- RSFC-20-1: Repository has an issue tracker

**Note**: These will be the identifiers needed to run single-test assessments. More information later in the README


## Requirements

Python 3.10.8 or higher

Dependencies are available in the requirements.txt or pyproject.toml file located in the root of the repository

## Install from PyPI

Just run in your terminal the following command:

```
pip install rsfc
```

## Install from Github with Poetry

To install the package, first clone the repository in your machine.
This project uses Poetry for dependency and environment management.

```
git clone https://github.com/oeg-upm/rsfc.git
```

Go to the project's root directory

```
cd rsfc
```

Install Poetry (if you haven’t already)

```
curl -sSL https://install.python-poetry.org | python3 -
```

Make sure Poetry is available in your PATH

```
poetry --version
```

Create the virtual environment and install dependencies

```
poetry install
```

Activate the virtual environment (Optional)

```
source $(poetry env info --path)/bin/activate
```

Your terminal prompt should now show something like:

```
(rsfc-py3.11) your-user@your-machine rsfc %
```

With virtual environment activated you can tried like this:

```
rsfc --help
```

Without poetry virtual environment activated you need to use the poetry run:

```
poetry run rsfc --help
```

## Usage

Before anything, RSFC uses SOMEF internally. If this is your first time working with somef, you should run the following command in the root directory of the project:

```
somef configure -a
```

Now, you can use the package by running if you activated the poetry env

```
rsfc --repo <repo_url>
```

or like this without the poetry env

```
poetry run rsfc --repo <repo_url>
```

If you want the output in OSTrails format, you can use the following flag

```
rsfc --repo <repo_url> --ftr
```

And additionally, if you want to run only one test, you can indicate the test identifier when running RSFC like this

```
rsfc --repo <repo_url> --id <test_id>
```

## Docker installation

RSFC also offers a Dockerfile which you can build using the following commmand:

```
docker build -t --no-cache -t rsfc-docker .
```

For comodity, we provide a bash script that runs the container along with the necessary configurations. To execute it just run

```
./run_rsfc.sh --repo <repo_url> [--ftr] [--id <test_id>]
```

The parameters used for the script are the same as if you executed RSFC normally

# RSFC GitHub Action

This repository provides a **reusable GitHub Action** to run RSFC on a given repository.

## Workflows

There are two key workflows:

- **`run-rsfc.yml`**:  
  Defines the main RSFC execution logic.  
  Note: This workflow cannot be triggered directly because it uses `on: workflow_call`.  
  It is designed to be reusable and must be invoked from another workflow.

- **`call-rsfc.yml`**:  
  A workflow file that triggers `run-rsfc.yml`. 
  It must be placed in each repository that you want to analyze, since the repository where `call-rsfc.yml` is hosted is the one that will be processed.  
  No additional inputs are required because the repository context is automatically passed by the `call`. 
  This workflow can be triggered manually (`workflow_dispatch`) or automatically (e.g., on `push` events).
  - **Secrets**:  
  - `RSFC_TOKEN` is optional but recommended if you plan to run multiple analyses or expect heavy usage. It allows RSFC to access private repositories and avoid rate limits. 


## Usage

To use RSFC in a repository:

1. Copy `call-rsfc.yml` into `.github/workflows/` of the repository you want to analyze.
2. Ensure that the required secrets are defined (see below).
3. No inputs are needed — the workflow automatically uses the repository it resides in.

Example:

```yaml
name: Call RSFC reusable workflow

on:
  workflow_dispatch:   
  push:                

jobs:
  call-rsfc:
    uses: oeg-upm/rsfc/.github/workflows/run-rsfc.yml@main
    with:
      repo_url: https://github.com/${{ github.repository }}
    secrets:
      RSFC_TOKEN: ${{ secrets.RSFC_TOKEN }}
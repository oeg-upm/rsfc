[![DOI](https://zenodo.org/badge/993095977.svg)](https://doi.org/10.5281/zenodo.16531481) [![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active) [![PyPI](https://img.shields.io/pypi/v/rsfc?label=PyPI)](https://pypi.org/project/rsfc/) [![RSFC_Coverage](https://img.shields.io/badge/rsfc-coverage_87%25-green)](./RSFC_REPORT.md)


# Research Software FAIRness Checks (RSFC)

A command line interface to automatically evaluate the fairness of a Github or Gitlab repository.

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
- has_contribution_guidelines
- software_is_containerized

For more information about these RSQIs, you can check https://github.com/EVERSE-ResearchSoftware/indicators. We have plans to implement all of the RSQIs available in that repository.


## Execution modes

RSFC offers the ability to run itself both in remote and local modes. Remote mode was the only execution mode available prior to version 0.1.8 and Local mode is an offline execution mode that uses the local path to your cloned repository instead of its Git URL.


## Available tests

RSFC offers a catalogue of its tests that you can check [here](https://oeg-upm.github.io/rsfc/doc/catalog.html#test)

**Note**: The short names stated in the catalogue will be the identifiers needed to run single-test assessments. More information later in the README


### Differences between execution modes

Remote and Local execution modes have different test lists due to ability/inability to perform HTTP requests. The differences are presented in the following table:

| TEST_ID | REMOTE | LOCAL |
|---|:---:|:---:|
| **RSFC-01-1** | x | |
| **RSFC-01-2** | x | x |
| **RSFC-01-3** | x | x |
| **RSFC-03-1** | x | |
| **RSFC-03-2** | x | |
| **RSFC-03-3** | x | |
| **RSFC-03-4** | x | |
| **RSFC-03-5** | x | |
| **RSFC-03-6** | x | x |
| **RSFC-04-1** | x | |
| **RSFC-04-2** | x | x |
| **RSFC-04-3** | x | x |
| **RSFC-04-4** | x | x |
| **RSFC-04-5** | x | |
| **RSFC-05-1** | x | x |
| **RSFC-05-2** | x | x |
| **RSFC-05-3** | x | x |
| **RSFC-06-1** | x | x |
| **RSFC-06-2** | x | x |
| **RSFC-06-3** | x | x |
| **RSFC-07-1** | x | x |
| **RSFC-07-2** | x | |
| **RSFC-08-1** | x | x |
| **RSFC-09-1** | x | |
| **RSFC-12-1** | x | x |
| **RSFC-13-1** | x | x |
| **RSFC-13-2** | x | x |
| **RSFC-13-3** | x | x |
| **RSFC-13-4** | x | x |
| **RSFC-14-1** | x | |
| **RSFC-14-2** | x | x |
| **RSFC-15-1** | x | x |
| **RSFC-15-2** | x | x |
| **RSFC-16-1** | x | x |
| **RSFC-17-2** | x | |
| **RSFC-17-3** | x | |
| **RSFC-18-1** | x | x |
| **RSFC-19-1** | x | x |
| **RSFC-20-1** | x | |
| **RSFC-21-1** | x | x |
| **RSFC-22-1** | x | x |


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

RSFC also offers the possibility of using a personal Github token to avoid a rate limit issue with the Github API

```
rsfc --repo <repo_url> -t <token>
```

### Parameter overview

Here is an overview of the available parameters supported by RSFC

```
Usage: rsfc [OPTIONS]

  RSFC - EVERSE Research Software Fairness Checks

Options:
  --repo TEXT        URL of the Github/Gitlab repository to be analyzed
  --local DIRECTORY  Local path of the repository to be analyzed
  -b TEXT            Name of the repo branch to analyze. By default
                     main/master
  -v TEXT            Tag of the release to analyze. By default latest release.
  --ftr              Flag to indicate if JSON-LD in FTR format is desired
  --id TEXT          Identifier of a specific test. Only that test will be ran
  --metadata FILE    SOMEF metadata file in case you already have one
  -t TEXT            Authorization Github token
  --help             Show this message and exit.
```

## RSFC Badge

Below the output table you will find a README badge that states what the total FAIR coverage you got in your assessment. It is already adapted to Markdown so you will just need to copy it.

### How is the coverage calculated?

The coverage is simply the rounded average percentage of the total tests passed. For example, if you passed 20 tests, the coverage will be (20/33)*100 = 61%

## Docker installation

RSFC also offers a Dockerfile which you can build using the following commmand:

```
docker build -t --no-cache -t rsfc-docker .
```

For comodity, we provide a bash script that runs the container along with the necessary configurations. To execute it just run

```
./run_rsfc.sh --repo <repo_url> [--ftr] [--id <test_id>] [-t <token>]
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

- **`use-rsfc.yml`**:  
  A workflow file that triggers `run-rsfc.yml`. 
  It must be placed in each repository that you want to analyze, since the repository where `use-rsfc.yml` is hosted is the one that will be processed.  
  No additional inputs are required because the repository context is automatically passed by the `call`. 
  This workflow can be triggered manually (`workflow_dispatch`) or automatically (e.g., on `push` events).
  - **Secrets**:  
  - `RSFC_TOKEN` is optional but recommended if you plan to run multiple analyses or expect heavy usage. It allows RSFC to access private repositories and avoid rate limits. 


## Usage

To use RSFC in a repository:

1. Copy `use-rsfc.yml` into `.github/workflows/` of the repository you want to analyze.
2. Ensure that the required secrets are defined (see below).
3. No inputs are needed — the workflow automatically uses the repository it resides in.


## Viewing RSFC Results in a Pull Request

When a Pull Request is opened or updated, the RSFC workflow runs automatically and adds a neutral check named **RSFC Results Summary**.

This check displays:
- the formatted RSFC console output, including the full assessment table  
- a link to the workflow job that executed the analysis  

### Accessing the JSON report

The workflow also generates an artifact named **`rsfc_assessment.json`**.

To download it:
1. Open the **Checks** tab of the Pull Request  
2. Select the job **Run RSFC Analysis**  
3. Download the artifact from the **Artifacts** section  

Example:

```yaml
name: Run RSFC analysis

on:
  workflow_dispatch: 
  pull_request: 
    types: [opened, synchronize, reopened]         

jobs:
  run-rsfc-checks:
    uses: oeg-upm/rsfc/.github/workflows/run-rsfc.yml@main
    with:
      repo_url: https://github.com/${{ github.repository }}
      is_fork: ${{ github.event.pull_request.head.repo.full_name != github.repository }}
      pr_sha: ${{ github.event.pull_request.head.sha }}
    secrets:
      RSFC_TOKEN: ${{ secrets.RSFC_TOKEN }}

# Quality Assessment for agnpy 0.5.1

An automated assessment of the agnpy tool based on the EVERSE software quality indicators, run on 2026-09-14.

## General Information

- **Software:** agnpy
- **Repository:** https://github.com/cosimoNigro/agnpy
- **Assessment date:** 2026-09-14T13:36:21Z
- **Total checks:** 41

## Summary

- **Passed (`true`)**: 35
- **Failed (`false`)**: 6
- **Errors (`error`)**: 0

## Results Table

| TEST ID | Short Description | Output |
| --- | --- | --- |
| [RSFC-01-1](https://w3id.org/rsfc/test/RSFC-01-1) | There is an identifier and it resolves | true |
| [RSFC-01-2](https://w3id.org/rsfc/test/RSFC-01-2) | There is an identifier in the metadata files | true |
| [RSFC-01-3](https://w3id.org/rsfc/test/RSFC-01-3) | There is an identifier and it follows a common schema | true |
| [RSFC-03-1](https://w3id.org/rsfc/test/RSFC-03-1) | The software has releases | true |
| [RSFC-03-2](https://w3id.org/rsfc/test/RSFC-03-2) | Releases have version and identifier | true |
| [RSFC-03-3](https://w3id.org/rsfc/test/RSFC-03-3) | Release versions follow SemVer or CalVer | true |
| [RSFC-03-4](https://w3id.org/rsfc/test/RSFC-03-4) | Release identifiers follow the same scheme | true |
| [RSFC-03-5](https://w3id.org/rsfc/test/RSFC-03-5) | Last release version corresponds to version in package file | true |
| [RSFC-03-6](https://w3id.org/rsfc/test/RSFC-03-6) | There is a version number stated in metadata files | true |
| [RSFC-04-1](https://w3id.org/rsfc/test/RSFC-04-1) | Metadata files exist | true |
| [RSFC-04-2](https://w3id.org/rsfc/test/RSFC-04-2) | There is a README file | true |
| [RSFC-04-3](https://w3id.org/rsfc/test/RSFC-04-3) | Title and description are declared | true |
| [RSFC-04-4](https://w3id.org/rsfc/test/RSFC-04-4) | There is descriptive metadata | true |
| [RSFC-04-5](https://w3id.org/rsfc/test/RSFC-04-5) | There is a codemeta file | true |
| [RSFC-05-1](https://w3id.org/rsfc/test/RSFC-05-1) | There is a repostatus badge in the README file | false |
| [RSFC-05-2](https://w3id.org/rsfc/test/RSFC-05-2) | Contact and support metadata exists | false |
| [RSFC-05-3](https://w3id.org/rsfc/test/RSFC-05-3) | Software documentation exists | true |
| [RSFC-06-1](https://w3id.org/rsfc/test/RSFC-06-1) | Authors are declared | true |
| [RSFC-06-2](https://w3id.org/rsfc/test/RSFC-06-2) | Contributors are declared | true |
| [RSFC-06-3](https://w3id.org/rsfc/test/RSFC-06-3) | Authors have an ORCID assigned | true |
| [RSFC-07-1](https://w3id.org/rsfc/test/RSFC-07-1) | There is an identifier in README or CITATION | true |
| [RSFC-07-2](https://w3id.org/rsfc/test/RSFC-07-2) | Software identifier resolves and links back to software | true |
| [RSFC-08-1](https://w3id.org/rsfc/test/RSFC-08-1) | Metadata record is found in SWHeritage or Zenodo | true |
| [RSFC-09-1](https://w3id.org/rsfc/test/RSFC-09-1) | Repository is from Github or Gitlab | true |
| [RSFC-12-1](https://w3id.org/rsfc/test/RSFC-12-1) | There is an article citation or reference publication | true |
| [RSFC-13-1](https://w3id.org/rsfc/test/RSFC-13-1) | Dependencies are declared | true |
| [RSFC-13-2](https://w3id.org/rsfc/test/RSFC-13-2) | There are installation instructions | true |
| [RSFC-13-3](https://w3id.org/rsfc/test/RSFC-13-3) | Dependencies have version numbers | false |
| [RSFC-13-4](https://w3id.org/rsfc/test/RSFC-13-4) | Dependencies are in a machine-readable format | true |
| [RSFC-14-1](https://w3id.org/rsfc/test/RSFC-14-1) | Tests are provided | true |
| [RSFC-14-2](https://w3id.org/rsfc/test/RSFC-14-2) | There are actions to automate tests | true |
| [RSFC-15-1](https://w3id.org/rsfc/test/RSFC-15-1) | There is a license | true |
| [RSFC-15-2](https://w3id.org/rsfc/test/RSFC-15-2) | License is in SPDX format | true |
| [RSFC-16-1](https://w3id.org/rsfc/test/RSFC-16-1) | License is referenced in metadata files | true |
| [RSFC-17-2](https://w3id.org/rsfc/test/RSFC-17-2) | Repository has a commit history | true |
| [RSFC-17-3](https://w3id.org/rsfc/test/RSFC-17-3) | Commits are linked to issues | false |
| [RSFC-18-1](https://w3id.org/rsfc/test/RSFC-18-1) | There are citations | true |
| [RSFC-19-1](https://w3id.org/rsfc/test/RSFC-19-1) | Repository has continuous integration workflows | true |
| [RSFC-20-1](https://w3id.org/rsfc/test/RSFC-20-1) | Repository has an issue tracker | true |
| [RSFC-21-1](https://w3id.org/rsfc/test/RSFC-21-1) | Repository has contribution guidelines | false |
| [RSFC-22-1](https://w3id.org/rsfc/test/RSFC-22-1) | Software offers a container file to run it | false |

## Detailed Results by Indicator

### archived_in_software_heritage

<a id="archived_in_software_heritage-https---w3id-org-rsfc-test-rsfc-08-1"></a>
#### Metadata record in Software Heritage or Zenodo

- **Test ID:** https://w3id.org/rsfc/test/RSFC-08-1
- **Result:** true
- **Process:** Searches for Zenodo and Software Heritage badges in the README file of the repository
- **Evidence:** A Zenodo DOI identifier was found in:
	- 10.5281/zenodo.4055175
	- https://doi.org/10.5281/zenodo.4055175
- **Suggestions:** N/A

### descriptive_metadata

<a id="descriptive_metadata-https---w3id-org-rsfc-test-rsfc-03-6"></a>
#### Version number in metadata

- **Test ID:** https://w3id.org/rsfc/test/RSFC-03-6
- **Result:** true
- **Process:** Checks if a version number for the software is indicated in the CITATION.cff, codemeta.json or package files(i.e. pyproject.toml, pom.xml, etc.)
- **Evidence:** Found the software version in:
	- https://raw.githubusercontent.com/cosimoNigro/agnpy/master/codemeta.json
	- https://raw.githubusercontent.com/cosimoNigro/agnpy/master/pyproject.toml
- **Suggestions:** N/A

<a id="descriptive_metadata-https---w3id-org-rsfc-test-rsfc-04-1"></a>
#### Metadata exists

- **Test ID:** https://w3id.org/rsfc/test/RSFC-04-1
- **Result:** true
- **Process:** Searches for codemeta, citation and package files in the repository
- **Evidence:** Found codemeta.json, package_file in the repository
- **Suggestions:** N/A

<a id="descriptive_metadata-https---w3id-org-rsfc-test-rsfc-04-3"></a>
#### There are title and description

- **Test ID:** https://w3id.org/rsfc/test/RSFC-04-3
- **Result:** true
- **Process:** Checks if there is a title and a description for the software in the metadata
- **Evidence:** A title was found in [https://raw.githubusercontent.com/cosimoNigro/agnpy/master/README.md] and a description was found in [https://raw.githubusercontent.com/cosimoNigro/agnpy/master/pyproject.toml]
- **Suggestions:** N/A

<a id="descriptive_metadata-https---w3id-org-rsfc-test-rsfc-04-4"></a>
#### Software has descriptive metadata

- **Test ID:** https://w3id.org/rsfc/test/RSFC-04-4
- **Result:** true
- **Process:** Searches for description, programming languages, date of creation and keywords in the repository
- **Evidence:** Descriptive metadata found in: Description [https://raw.githubusercontent.com/cosimoNigro/agnpy/master/README.md, https://raw.githubusercontent.com/cosimoNigro/agnpy/master/codemeta.json, https://raw.githubusercontent.com/cosimoNigro/agnpy/master/pyproject.toml], Languages [https://raw.githubusercontent.com/cosimoNigro/agnpy/master/codemeta.json], Date Created [https://raw.githubusercontent.com/cosimoNigro/agnpy/master/codemeta.json], Keywords [https://raw.githubusercontent.com/cosimoNigro/agnpy/master/codemeta.json]
- **Suggestions:** N/A

<a id="descriptive_metadata-https---w3id-org-rsfc-test-rsfc-04-5"></a>
#### There is a codemeta file

- **Test ID:** https://w3id.org/rsfc/test/RSFC-04-5
- **Result:** true
- **Process:** Searches for a codemeta.json file in the repository
- **Evidence:** A codemeta.json file was found in the root of the repository
- **Suggestions:** N/A

<a id="descriptive_metadata-https---w3id-org-rsfc-test-rsfc-06-1"></a>
#### Authors are declared

- **Test ID:** https://w3id.org/rsfc/test/RSFC-06-1
- **Result:** true
- **Process:** Searches for authors in various files of the repository (i.e. CITATION.cff, AUTHORS.md, codemeta.json)
- **Evidence:** Authors were found in:
	- https://raw.githubusercontent.com/cosimoNigro/agnpy/master/codemeta.json
	- https://raw.githubusercontent.com/cosimoNigro/agnpy/master/pyproject.toml
- **Suggestions:** N/A

<a id="descriptive_metadata-https---w3id-org-rsfc-test-rsfc-06-2"></a>
#### Contributors are declared

- **Test ID:** https://w3id.org/rsfc/test/RSFC-06-2
- **Result:** true
- **Process:** Searches for contributors in various files of the repository (i.e. codemeta.json, pyproject.toml, pom.xml)'
- **Evidence:** Contributors were found in:
	- https://raw.githubusercontent.com/cosimoNigro/agnpy/master/codemeta.json
- **Suggestions:** N/A

<a id="descriptive_metadata-https---w3id-org-rsfc-test-rsfc-06-3"></a>
#### Authors have an ORCID

- **Test ID:** https://w3id.org/rsfc/test/RSFC-06-3
- **Result:** true
- **Process:** Checks if all authors stated in the CITATION.cff file have an ORCID assigned
- **Evidence:** All authors in both the codemeta.json and CITATION.cff files have an orcid identifier
- **Suggestions:** N/A

### has_contribution_guidelines

<a id="has_contribution_guidelines-https---w3id-org-rsfc-test-rsfc-21-1"></a>
#### Repository has contribution guidelines

- **Test ID:** https://w3id.org/rsfc/test/RSFC-21-1
- **Result:** false
- **Process:** Checks if there are contribution guidelines either in the README file or if there is a CONTRIBUTING.md file
- **Evidence:** Could not find contribution guidelines in the repository
- **Suggestions:** If you want to properly keep track of the colaborations your project receives to ensure its quality and fiability, you should add some contribution guidelines so the colaborators know how you want contributions to be made

### has_releases

<a id="has_releases-https---w3id-org-rsfc-test-rsfc-03-1"></a>
#### Software has releases

- **Test ID:** https://w3id.org/rsfc/test/RSFC-03-1
- **Result:** true
- **Process:** Searches for release tags in the repository
- **Evidence:** These releases were found:
	- https://github.com/cosimoNigro/agnpy/releases/tag/v0.5.1
	- https://github.com/cosimoNigro/agnpy/releases/tag/v0.5.0
	- https://github.com/cosimoNigro/agnpy/releases/tag/v0.4.0
	- https://github.com/cosimoNigro/agnpy/releases/tag/v0.3.0
	- https://github.com/cosimoNigro/agnpy/releases/tag/v0.2.0
	- https://github.com/cosimoNigro/agnpy/releases/tag/v0.1.8
	- https://github.com/cosimoNigro/agnpy/releases/tag/v0.1.7
	- https://github.com/cosimoNigro/agnpy/releases/tag/v0.1.6
	- https://github.com/cosimoNigro/agnpy/releases/tag/v0.1.4
	- https://github.com/cosimoNigro/agnpy/releases/tag/v0.1.3
	- https://github.com/cosimoNigro/agnpy/releases/tag/v0.1.2
	- https://github.com/cosimoNigro/agnpy/releases/tag/v0.1.1
	- https://github.com/cosimoNigro/agnpy/releases/tag/v0.1.0
	- https://github.com/cosimoNigro/agnpy/releases/tag/v0.0.10
	- https://github.com/cosimoNigro/agnpy/releases/tag/v0.0.8
	- https://github.com/cosimoNigro/agnpy/releases/tag/v0.0.7.3
	- https://github.com/cosimoNigro/agnpy/releases/tag/v0.0.7.2
	- https://github.com/cosimoNigro/agnpy/releases/tag/v0.0.7
- **Suggestions:** N/A

<a id="has_releases-https---w3id-org-rsfc-test-rsfc-03-2"></a>
#### Releases have an id and version number

- **Test ID:** https://w3id.org/rsfc/test/RSFC-03-2
- **Result:** true
- **Process:** Checks if all of the releases have an identifier and a version
- **Evidence:** All of the releases have an id and a version
- **Suggestions:** N/A

<a id="has_releases-https---w3id-org-rsfc-test-rsfc-03-4"></a>
#### Release identifiers follow the same scheme

- **Test ID:** https://w3id.org/rsfc/test/RSFC-03-4
- **Result:** true
- **Process:** Checks if all of the version identifiers follow the same scheme
- **Evidence:** All of the releases URLs follow the same scheme
- **Suggestions:** N/A

<a id="has_releases-https---w3id-org-rsfc-test-rsfc-03-5"></a>
#### Last release consistency

- **Test ID:** https://w3id.org/rsfc/test/RSFC-03-5
- **Result:** true
- **Process:** Checks if the latest release tag matches the version stated in the codemeta or package files of the repository
- **Evidence:** Latest release matches the latest version stated in the metadata files
- **Suggestions:** N/A

### persistent_and_unique_identifier

<a id="persistent_and_unique_identifier-https---w3id-org-rsfc-test-rsfc-01-1"></a>
#### There is an identifier and resolves

- **Test ID:** https://w3id.org/rsfc/test/RSFC-01-1
- **Result:** true
- **Process:** Searches for an identifier (i.e. DOI or SWHID) in the README file of the repository
- **Evidence:** Found the identifier https://doi.org/10.5281/zenodo.4055175 in the README and it resolves
- **Suggestions:** N/A

<a id="persistent_and_unique_identifier-https---w3id-org-rsfc-test-rsfc-01-2"></a>
#### There is an identifier associated with the software

- **Test ID:** https://w3id.org/rsfc/test/RSFC-01-2
- **Result:** true
- **Process:** Searches for an identifier in the CITATION.cff, codemeta.json and README files
- **Evidence:** An identifier was found in README.md, codemeta.json. However, no identifier was found in CITATION.cff.
- **Suggestions:** N/A

<a id="persistent_and_unique_identifier-https---w3id-org-rsfc-test-rsfc-01-3"></a>
#### Software identifier follows a proper schema

- **Test ID:** https://w3id.org/rsfc/test/RSFC-01-3
- **Result:** true
- **Process:** Checks if the identifiers associated with the software follow any of these schemas: DOI, URN, GITHUB and SWHID
- **Evidence:** All of the identifiers detected follow a common schema
- **Suggestions:** N/A

<a id="persistent_and_unique_identifier-https---w3id-org-rsfc-test-rsfc-07-1"></a>
#### There is an identifier in README or CITATION.cff

- **Test ID:** https://w3id.org/rsfc/test/RSFC-07-1
- **Result:** true
- **Process:** Searches for an identifier in the README or CITATION.cff files of the repository
- **Evidence:** An identifier was found in the README file of the repository
	- https://doi.org/10.5281/zenodo.4055175
- **Suggestions:** N/A

<a id="persistent_and_unique_identifier-https---w3id-org-rsfc-test-rsfc-07-2"></a>
#### Software identifier resolves to software

- **Test ID:** https://w3id.org/rsfc/test/RSFC-07-2
- **Result:** true
- **Process:** Checks if the identifier found in the README file or metadata files (i.e. codemeta.json, CITATION.cff) resolves to a page that links back to the software repository
- **Evidence:** The landing page of the software's identifier 10.5281/zenodo.4055175 links back to the software repository
- **Suggestions:** N/A

### repository_workflows

<a id="repository_workflows-https---w3id-org-rsfc-test-rsfc-14-2"></a>
#### There are actions to automate tests

- **Test ID:** https://w3id.org/rsfc/test/RSFC-14-2
- **Result:** true
- **Process:** Searches for workflows that contain test or tests in their names
- **Evidence:** There are workflows or actions that perform automated tests
	- https://raw.githubusercontent.com/cosimoNigro/agnpy/master/.github/workflows/test.yml
- **Suggestions:** N/A

<a id="repository_workflows-https---w3id-org-rsfc-test-rsfc-19-1"></a>
#### Repository has workflows

- **Test ID:** https://w3id.org/rsfc/test/RSFC-19-1
- **Result:** true
- **Process:** Searches for workflows in the repository
- **Evidence:** Workflows were found in:
	- https://raw.githubusercontent.com/cosimoNigro/agnpy/master/.github/workflows/pypi-upload.yml
	- https://raw.githubusercontent.com/cosimoNigro/agnpy/master/.github/workflows/test.yml
- **Suggestions:** N/A

### requirements_specified

<a id="requirements_specified-https---w3id-org-rsfc-test-rsfc-13-1"></a>
#### Dependencies are declared

- **Test ID:** https://w3id.org/rsfc/test/RSFC-13-1
- **Result:** true
- **Process:** Searches for dependencies in project configuration files, README and dependencies files such as requirements.txt
- **Evidence:** Requirements were found in:
	- https://raw.githubusercontent.com/cosimoNigro/agnpy/master/codemeta.json
	- https://raw.githubusercontent.com/cosimoNigro/agnpy/master/environment.yml
	- https://raw.githubusercontent.com/cosimoNigro/agnpy/master/pyproject.toml
	- https://raw.githubusercontent.com/cosimoNigro/agnpy/master/docs/requirements.txt
	- https://raw.githubusercontent.com/cosimoNigro/agnpy/master/README.md
- **Suggestions:** N/A

<a id="requirements_specified-https---w3id-org-rsfc-test-rsfc-13-3"></a>
#### Dependencies have version numbers

- **Test ID:** https://w3id.org/rsfc/test/RSFC-13-3
- **Result:** false
- **Process:** Checks if all of the dependencies stated in the machine-readable file (e.g. requirements.txt, pyproject.toml, etc.) of the repository have a version indicated
- **Evidence:** The following dependencies do not have a version stated:
	- Unknown dependency
	- pip
	- -e .
	- pre-commit
	- wheel
	- sphinx-astropy
	- nbsphinx
	- ipython
	- ipykernel
	- docutils
- **Suggestions:** All of your dependencies should have their versions stated to ensure its reproducibility. More information at https://everse.software/RSQKit/reproducible_software_environments

<a id="requirements_specified-https---w3id-org-rsfc-test-rsfc-13-4"></a>
#### There is a dependencies machine-readable file

- **Test ID:** https://w3id.org/rsfc/test/RSFC-13-4
- **Result:** true
- **Process:** Checks if dependencies are indicated in a machine-readable file
- **Evidence:** There is a machine-readable file for dependencies at:
	- https://raw.githubusercontent.com/cosimoNigro/agnpy/master/codemeta.json
	- https://raw.githubusercontent.com/cosimoNigro/agnpy/master/environment.yml
	- https://raw.githubusercontent.com/cosimoNigro/agnpy/master/environment.yml
	- https://raw.githubusercontent.com/cosimoNigro/agnpy/master/environment.yml
	- https://raw.githubusercontent.com/cosimoNigro/agnpy/master/pyproject.toml
	- https://raw.githubusercontent.com/cosimoNigro/agnpy/master/pyproject.toml
	- https://raw.githubusercontent.com/cosimoNigro/agnpy/master/pyproject.toml
	- https://raw.githubusercontent.com/cosimoNigro/agnpy/master/pyproject.toml
	- https://raw.githubusercontent.com/cosimoNigro/agnpy/master/pyproject.toml
	- https://raw.githubusercontent.com/cosimoNigro/agnpy/master/pyproject.toml
	- https://raw.githubusercontent.com/cosimoNigro/agnpy/master/pyproject.toml
	- https://raw.githubusercontent.com/cosimoNigro/agnpy/master/pyproject.toml
	- https://raw.githubusercontent.com/cosimoNigro/agnpy/master/pyproject.toml
	- https://raw.githubusercontent.com/cosimoNigro/agnpy/master/docs/requirements.txt
	- https://raw.githubusercontent.com/cosimoNigro/agnpy/master/docs/requirements.txt
	- https://raw.githubusercontent.com/cosimoNigro/agnpy/master/docs/requirements.txt
	- https://raw.githubusercontent.com/cosimoNigro/agnpy/master/docs/requirements.txt
	- https://raw.githubusercontent.com/cosimoNigro/agnpy/master/docs/requirements.txt
	- https://raw.githubusercontent.com/cosimoNigro/agnpy/master/docs/requirements.txt
	- https://raw.githubusercontent.com/cosimoNigro/agnpy/master/docs/requirements.txt
- **Suggestions:** N/A

### software_has_citation

<a id="software_has_citation-https---w3id-org-rsfc-test-rsfc-12-1"></a>
#### There is an article citation or reference publication

- **Test ID:** https://w3id.org/rsfc/test/RSFC-12-1
- **Result:** true
- **Process:** Searches for an article citation or a reference publication in the codemeta and citation files
- **Evidence:** A reference publication was found in:
	- Untitled Citation
- **Suggestions:** N/A

<a id="software_has_citation-https---w3id-org-rsfc-test-rsfc-18-1"></a>
#### Repository has citation

- **Test ID:** https://w3id.org/rsfc/test/RSFC-18-1
- **Result:** true
- **Process:** Searches for a CITATION.cff file and README file in the repository
- **Evidence:** A citation was found in:
	- https://raw.githubusercontent.com/cosimoNigro/agnpy/master/README.md
	- https://raw.githubusercontent.com/cosimoNigro/agnpy/master/codemeta.json
- **Suggestions:** N/A

### software_has_documentation

<a id="software_has_documentation-https---w3id-org-rsfc-test-rsfc-04-2"></a>
#### There is a README

- **Test ID:** https://w3id.org/rsfc/test/RSFC-04-2
- **Result:** true
- **Process:** Searches for a README file in the repository
- **Evidence:** There is a README file in the repository
- **Suggestions:** N/A

<a id="software_has_documentation-https---w3id-org-rsfc-test-rsfc-05-2"></a>
#### There is contact and/or support metadata

- **Test ID:** https://w3id.org/rsfc/test/RSFC-05-2
- **Result:** false
- **Process:** Searches for contact and support information in the repository
- **Evidence:** Could not find any contact or support information in the repository
- **Suggestions:** You should include contact information in your software's metadata in case someone wants to ask for information.

<a id="software_has_documentation-https---w3id-org-rsfc-test-rsfc-05-3"></a>
#### Software documentation

- **Test ID:** https://w3id.org/rsfc/test/RSFC-05-3
- **Result:** true
- **Process:** Searches for a README file in the root repository and other forms of documentation such as a Read The Docs badge or url
- **Evidence:** Documentation was found in:
	- https://agnpy.readthedocs.io/en/latest/
	- https://raw.githubusercontent.com/cosimoNigro/agnpy/master/README.md
- **Suggestions:** N/A

<a id="software_has_documentation-https---w3id-org-rsfc-test-rsfc-13-2"></a>
#### There are installation instructions

- **Test ID:** https://w3id.org/rsfc/test/RSFC-13-2
- **Result:** true
- **Process:** Searches for installation instructions in the README file of the repository
- **Evidence:** Installation instructions were found in:
	- https://raw.githubusercontent.com/cosimoNigro/agnpy/master/README.md
- **Suggestions:** N/A

### software_has_license

<a id="software_has_license-https---w3id-org-rsfc-test-rsfc-15-1"></a>
#### Software has license

- **Test ID:** https://w3id.org/rsfc/test/RSFC-15-1
- **Result:** true
- **Process:** Searches for a file named 'LICENSE' or 'LICENSE.md' in the root of the repository.
- **Evidence:** A license was found in:
	- https://raw.githubusercontent.com/cosimoNigro/agnpy/master/codemeta.json
	- https://raw.githubusercontent.com/cosimoNigro/agnpy/master/LICENSE
- **Suggestions:** N/A

<a id="software_has_license-https---w3id-org-rsfc-test-rsfc-15-2"></a>
#### License is SPDX compliant

- **Test ID:** https://w3id.org/rsfc/test/RSFC-15-2
- **Result:** true
- **Process:** Checks if the licenses detected are SPDX compliant
- **Evidence:** All licenses are SPDX compliant
- **Suggestions:** N/A

<a id="software_has_license-https---w3id-org-rsfc-test-rsfc-16-1"></a>
#### License referenced in metadata files

- **Test ID:** https://w3id.org/rsfc/test/RSFC-16-1
- **Result:** true
- **Process:** Searches for licensing information in the codemeta, CITATION.cff and package files if they exist
- **Evidence:** Found license information in codemeta (BSD-3-Clause) but could not find any in CITATION.cff, package
- **Suggestions:** N/A

### software_has_tests

<a id="software_has_tests-https---w3id-org-rsfc-test-rsfc-14-1"></a>
#### Presence of tests in repository

- **Test ID:** https://w3id.org/rsfc/test/RSFC-14-1
- **Result:** true
- **Process:** Searches for files and/or directories that mention test in their names. Also, ignores doc and docs directories
- **Evidence:** Files and/or directories that mention test were found at:
	- .github/workflows/test.yml
	- agnpy/absorption/tests
	- agnpy/absorption/tests/__init__.py
	- agnpy/absorption/tests/test_absorption.py
	- agnpy/compton/tests
	- agnpy/compton/tests/__init__.py
	- agnpy/compton/tests/test_compton.py
	- agnpy/constraints/tests
	- agnpy/constraints/tests/__init__.py
	- agnpy/constraints/tests/test_constraints.py
	- agnpy/data/reference_seds/cerruti_psynch/test_pss.dat
	- agnpy/emission_regions/tests
	- agnpy/emission_regions/tests/__init__.py
	- agnpy/emission_regions/tests/test_emission_regions.py
	- agnpy/fit/tests
	- agnpy/fit/tests/__init__.py
	- agnpy/fit/tests/test_fit.py
	- agnpy/fit/tests/test_wrappers.py
	- agnpy/photo_meson/tests
	- agnpy/photo_meson/tests/__init__.py
	- agnpy/photo_meson/tests/test_photo_meson.py
	- agnpy/radiative_process/tests
	- agnpy/radiative_process/tests/__init__.py
	- agnpy/radiative_process/tests/test_radiative_process.py
	- agnpy/spectra/tests
	- agnpy/spectra/tests/__init__.py
	- agnpy/spectra/tests/test_spectra.py
	- agnpy/synchrotron/tests
	- agnpy/synchrotron/tests/__init__.py
	- agnpy/synchrotron/tests/test_proton_synchrotron.py
	- agnpy/synchrotron/tests/test_synchrotron.py
	- agnpy/targets/tests
	- agnpy/targets/tests/__init__.py
	- agnpy/targets/tests/test_targets.py
	- agnpy/time_evolution/tests
	- agnpy/time_evolution/tests/__init__.py
	- agnpy/time_evolution/tests/out_0.3e45erg_gamma1e4to1e7_homogenous_eed_evol.txt
	- agnpy/time_evolution/tests/out_escape_to_blob_B=10.30_tacc=1.000000e+01_tesc=1.000000e+01_no_merging.txt
	- agnpy/time_evolution/tests/out_inject_continuous_B=10.10_tacc=5.000000e+00.txt
	- agnpy/time_evolution/tests/test_blob_expansion.py
	- agnpy/time_evolution/tests/test_blob_ltt_integration.py
	- agnpy/time_evolution/tests/test_time_evolution.py
	- agnpy/time_evolution/tests/test_time_evolution_utils.py
	- agnpy/utils/tests
	- agnpy/utils/tests/__init__.py
	- agnpy/utils/tests/test_utils.py
	- experiments/basic/trapz_loglog_test.ipynb
- **Suggestions:** N/A

### software_is_containerized

<a id="software_is_containerized-https---w3id-org-rsfc-test-rsfc-22-1"></a>
#### Software is containerized

- **Test ID:** https://w3id.org/rsfc/test/RSFC-22-1
- **Result:** false
- **Process:** Searches in the root of the repository for container files such as dockerfile, apptainer, podman, etc.
- **Evidence:** Could not find any container file in the repository
- **Suggestions:** You should allow interopertability when other users want to execute your software easily

### support_issue_tracking

<a id="support_issue_tracking-https---w3id-org-rsfc-test-rsfc-20-1"></a>
#### Repository has an issue tracker

- **Test ID:** https://w3id.org/rsfc/test/RSFC-20-1
- **Result:** true
- **Process:** Checks if there is an issue tracker in the repository.
- **Evidence:** Found an issue tracker in the repository at:
	- https://raw.githubusercontent.com/cosimoNigro/agnpy/master/codemeta.json
- **Suggestions:** N/A

### version_control_use

<a id="version_control_use-https---w3id-org-rsfc-test-rsfc-05-1"></a>
#### There is a repostatus badge

- **Test ID:** https://w3id.org/rsfc/test/RSFC-05-1
- **Result:** false
- **Process:** Searches for a repo status badge in the README file of the repository
- **Evidence:** Could not find a repo status badge in the repository
- **Suggestions:** You should include the state of your repository in the README file

<a id="version_control_use-https---w3id-org-rsfc-test-rsfc-09-1"></a>
#### Repository is from Github/Gitlab

- **Test ID:** https://w3id.org/rsfc/test/RSFC-09-1
- **Result:** true
- **Process:** Checks if the URL provided is indeed a Github or Gitlab repository
- **Evidence:** URL provided is a Github or Gitlab repository
- **Suggestions:** N/A

<a id="version_control_use-https---w3id-org-rsfc-test-rsfc-17-2"></a>
#### Commit history

- **Test ID:** https://w3id.org/rsfc/test/RSFC-17-2
- **Result:** true
- **Process:** Checks if the software repository has a commits history
- **Evidence:** A commit history was found in:
	- https://api.github.com/repos/cosimoNigro/agnpy/commits?sha=master&since=2026-06-16T13:36:10.923346+00:00&per_page=100
- **Suggestions:** N/A

<a id="version_control_use-https---w3id-org-rsfc-test-rsfc-17-3"></a>
#### Commits are linked to issues

- **Test ID:** https://w3id.org/rsfc/test/RSFC-17-3
- **Result:** false
- **Process:** Checks if there is at least one of the existing issues (opened or closed) referenced in any of the commits made in the default branch of the repository
- **Evidence:** There is not any commits linked to any issues in the repository
- **Suggestions:** It is good practice to indicate in your commits which issues you are targeting or solving

### versioning_standards_use

<a id="versioning_standards_use-https---w3id-org-rsfc-test-rsfc-03-3"></a>
#### Release versions follow a community established convention

- **Test ID:** https://w3id.org/rsfc/test/RSFC-03-3
- **Result:** true
- **Process:** Checks if all of the releases versions follow the SemVer or CalVer versioning standards
- **Evidence:** All of the releases follow a versioning standard
Note: Some versions did not follow the convention but passed the 80% threshold:
	- v0.0.7.3
	- v0.0.7.2
- **Suggestions:** N/A

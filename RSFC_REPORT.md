# Quality Assessment for rsfc v0.1.4

An automated assessment of the rsfc tool based on the EVERSE software quality indicators, run on 2026-04-13.

## General Information

- **Software:** rsfc
- **Repository:** https://github.com/oeg-upm/rsfc
- **Assessment date:** 2026-04-13T11:10:53Z
- **Total checks:** 42

## Summary

- **Passed (`true`)**: 32
- **Failed (`false`)**: 10
- **Errors (`error`)**: 0

## Results Table

| TEST ID | Short Description | Output |
| --- | --- | --- |
| RSFC-01-1 | There is an identifier and it resolves | true |
| RSFC-01-2 | There is an identifier in the metadata files | true |
| RSFC-01-3 | There is an identifier and it follows a common schema | true |
| RSFC-03-1 | The software has releases | true |
| RSFC-03-2 | Releases have version and identifier | true |
| RSFC-03-3 | Release versions follow SemVer or CalVer | true |
| RSFC-03-4 | Release identifiers follow the same scheme | true |
| RSFC-03-5 | Last release version corresponds to version in package file | false |
| RSFC-03-6 | There is a version number stated in metadata files | true |
| RSFC-04-1 | Metadata files exist | true |
| RSFC-04-2 | There is a README file | true |
| RSFC-04-3 | Title and description are declared | true |
| RSFC-04-4 | There is descriptive metadata | true |
| RSFC-04-5 | There is a codemeta file | true |
| RSFC-05-1 | There is a repostatus badge in the README file | true |
| RSFC-05-2 | Contact and support metadata exists | false |
| RSFC-05-3 | Software documentation exists | true |
| RSFC-06-1 | Authors are declared | true |
| RSFC-06-2 | Contributors are declared | false |
| RSFC-06-3 | Authors have an ORCID assigned | false |
| RSFC-06-4 | Authors have their roles stated | false |
| RSFC-07-1 | There is an identifier in README or CITATION | true |
| RSFC-07-2 | Software identifier resolves and links back to software | true |
| RSFC-08-1 | Metadata record is found in SWHeritage or Zenodo | true |
| RSFC-09-1 | Repository is from Github or Gitlab | true |
| RSFC-12-1 | There is an article citation or reference publication | false |
| RSFC-13-1 | Dependencies are declared | true |
| RSFC-13-2 | There are installation instructions | true |
| RSFC-13-3 | Dependencies have version numbers | false |
| RSFC-13-4 | Dependencies are in a machine-readable format | true |
| RSFC-14-1 | Tests are provided | true |
| RSFC-14-2 | There are actions to automate tests | false |
| RSFC-15-1 | There is a license | true |
| RSFC-15-2 | License is in SPDX format | false |
| RSFC-16-1 | License is referenced in metadata files | true |
| RSFC-17-1 | The repository has an 'active' status | true |
| RSFC-17-2 | Repository has a commit history | true |
| RSFC-17-3 | Commits are linked to issues | true |
| RSFC-18-1 | There are citations | true |
| RSFC-19-1 | Repository has continuous integration workflows | true |
| RSFC-20-1 | Repository has an issue tracker | true |
| RSFC-21-1 | Repository has contribution guidelines | false |

## Detailed Results by Indicator

### archived_in_software_heritage

<a id="archived_in_software_heritage-https---w3id-org-rsfc-test-rsfc-08-1"></a>
#### Metadata record in Software Heritage or Zenodo

- **Test ID:** https://w3id.org/rsfc/test/RSFC-08-1
- **Result:** true
- **Process:** Searches for Zenodo and Software Heritage badges in the README file of the repository
- **Evidence:** A Zenodo DOI identifier was found in the repository
- **Suggestions:** No suggestions

### descriptive_metadata

<a id="descriptive_metadata-https---w3id-org-rsfc-test-rsfc-03-6"></a>
#### Version number in metadata

- **Test ID:** https://w3id.org/rsfc/test/RSFC-03-6
- **Result:** true
- **Process:** Checks if a version number for the software is indicated in the CITATION.cff, codemeta.json or package files(i.e. pyproject.toml, pom.xml, etc.)
- **Evidence:** Found the software version in one of the specified files
- **Suggestions:** No suggestions

<a id="descriptive_metadata-https---w3id-org-rsfc-test-rsfc-04-1"></a>
#### Metadata exists

- **Test ID:** https://w3id.org/rsfc/test/RSFC-04-1
- **Result:** true
- **Process:** Searches for codemeta, citation and package files in the repository
- **Evidence:** Found codemeta, citation and package files in the repository
- **Suggestions:** No suggestions

<a id="descriptive_metadata-https---w3id-org-rsfc-test-rsfc-04-3"></a>
#### There are title and description

- **Test ID:** https://w3id.org/rsfc/test/RSFC-04-3
- **Result:** true
- **Process:** Checks if there is a title and a description for the software in the metadata
- **Evidence:** Title and description were found in the repository
- **Suggestions:** No suggestions

<a id="descriptive_metadata-https---w3id-org-rsfc-test-rsfc-04-4"></a>
#### Software has descriptive metadata

- **Test ID:** https://w3id.org/rsfc/test/RSFC-04-4
- **Result:** true
- **Process:** Searches for description, programming languages, date of creation and keywords in the repository
- **Evidence:** Descriptive metadata was found in the repository
- **Suggestions:** No suggestions

<a id="descriptive_metadata-https---w3id-org-rsfc-test-rsfc-04-5"></a>
#### There is a codemeta file

- **Test ID:** https://w3id.org/rsfc/test/RSFC-04-5
- **Result:** true
- **Process:** Searches for a codemeta.json file in the repository
- **Evidence:** A codemeta.json file was found in the root of the repository
- **Suggestions:** No suggestions

<a id="descriptive_metadata-https---w3id-org-rsfc-test-rsfc-06-1"></a>
#### Authors are declared

- **Test ID:** https://w3id.org/rsfc/test/RSFC-06-1
- **Result:** true
- **Process:** Searches for authors in various files of the repository (i.e. CITATION.cff, AUTHORS.md, codemeta.json)
- **Evidence:** Authors were found in the repository
- **Suggestions:** No suggestions

<a id="descriptive_metadata-https---w3id-org-rsfc-test-rsfc-06-2"></a>
#### Contributors are declared

- **Test ID:** https://w3id.org/rsfc/test/RSFC-06-2
- **Result:** false
- **Process:** Searches for contributors in various files of the repository (i.e. codemeta.json, pyproject.toml, pom.xml)'
- **Evidence:** Found authors but could not find any contributors in the repository
- **Suggestions:** Your software should also document its contributors if there are any. More information at https://everse.software/RSQKit/documenting_software_project

<a id="descriptive_metadata-https---w3id-org-rsfc-test-rsfc-06-3"></a>
#### Authors have an ORCID

- **Test ID:** https://w3id.org/rsfc/test/RSFC-06-3
- **Result:** false
- **Process:** Checks if all authors stated in the CITATION.cff file have an ORCID assigned
- **Evidence:** One or more authors do not have an ORCID assigned
- **Suggestions:** When documenting your software's authors, you should include their ORCIDs if possible.

<a id="descriptive_metadata-https---w3id-org-rsfc-test-rsfc-06-4"></a>
#### Authors have roles

- **Test ID:** https://w3id.org/rsfc/test/RSFC-06-4
- **Result:** false
- **Process:** Checks if all authors stated in a codemeta.json file have a role assigned 
- **Evidence:** There are one or more authors in the codemeta file that do not have roles assigned
- **Suggestions:** When documenting your software's authors, you should include their roles if possible.

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
	- RSFC-0.1.4
	- RSFC-0.1.3
	- RSFC-0.1.2
	- RSFC-0.1.1
	- RSFC-0.1.0
	- RSFC-0.0.9
	- RSFC-0.0.8
	- RSFC-0.0.7
	- RSFC-0.0.6
	- RSFC-0.0.5
	- RSFC-0.0.4
	- RSFC-0.0.3
	- RSFC-0.0.2
	- RSFC-0.0.1
- **Suggestions:** No suggestions

<a id="has_releases-https---w3id-org-rsfc-test-rsfc-03-2"></a>
#### Releases have an id and version number

- **Test ID:** https://w3id.org/rsfc/test/RSFC-03-2
- **Result:** true
- **Process:** Checks if all of the releases have an identifier and a version
- **Evidence:** All of the releases have an id and a version
- **Suggestions:** No suggestions

<a id="has_releases-https---w3id-org-rsfc-test-rsfc-03-4"></a>
#### Release identifiers follow the same scheme

- **Test ID:** https://w3id.org/rsfc/test/RSFC-03-4
- **Result:** true
- **Process:** Checks if all of the version identifiers follow the same scheme
- **Evidence:** All of the releases URLs follow the same scheme
- **Suggestions:** No suggestions

<a id="has_releases-https---w3id-org-rsfc-test-rsfc-03-5"></a>
#### Last release consistency

- **Test ID:** https://w3id.org/rsfc/test/RSFC-03-5
- **Result:** false
- **Process:** Checks if the latest release tag matches the version stated in the package file of the repository
- **Evidence:** Latest release does not match the latest version stated
- **Suggestions:** It is good practice to keep consistency between the version of your latest release and the version in your metadata files

### persistent_and_unique_identifier

<a id="persistent_and_unique_identifier-https---w3id-org-rsfc-test-rsfc-01-1"></a>
#### There is an identifier and resolves

- **Test ID:** https://w3id.org/rsfc/test/RSFC-01-1
- **Result:** true
- **Process:** Searches for an identifier (i.e. DOI or SWHID) in the README file of the repository
- **Evidence:** Found the identifier https://doi.org/10.5281/zenodo.16531481 in the README and it resolves
- **Suggestions:** No suggestions

<a id="persistent_and_unique_identifier-https---w3id-org-rsfc-test-rsfc-01-2"></a>
#### There is an identifier associated with the software

- **Test ID:** https://w3id.org/rsfc/test/RSFC-01-2
- **Result:** true
- **Process:** Searches for an identifier in the CITATION.cff, codemeta.json and README files
- **Evidence:** An identifier was found but could not find it in the following locations: 
- **Suggestions:** No suggestions

<a id="persistent_and_unique_identifier-https---w3id-org-rsfc-test-rsfc-01-3"></a>
#### Software identifier follows a proper schema

- **Test ID:** https://w3id.org/rsfc/test/RSFC-01-3
- **Result:** true
- **Process:** Checks if the identifiers associated with the software follow any of these schemas: DOI, URN, GITHUB and SWHID
- **Evidence:** All of the identifiers detected follow a common schema
- **Suggestions:** No suggestions

<a id="persistent_and_unique_identifier-https---w3id-org-rsfc-test-rsfc-07-1"></a>
#### There is an identifier in README or CITATION.cff

- **Test ID:** https://w3id.org/rsfc/test/RSFC-07-1
- **Result:** true
- **Process:** Searches for an identifier in the README or CITATION.cff files of the repository
- **Evidence:** An identifier was found in both the README and CITATION.cff files of the repository
- **Suggestions:** No suggestions

<a id="persistent_and_unique_identifier-https---w3id-org-rsfc-test-rsfc-07-2"></a>
#### Software identifier resolves to software

- **Test ID:** https://w3id.org/rsfc/test/RSFC-07-2
- **Result:** true
- **Process:** Checks if the identifier found in the README file or metadata files (i.e. codemeta.json, CITATION.cff) resolves to a page that links back to the software repository
- **Evidence:** The landing page of the software's identifier links back to the software repository
- **Suggestions:** No suggestions

### repository_workflows

<a id="repository_workflows-https---w3id-org-rsfc-test-rsfc-14-2"></a>
#### There are actions to automate tests

- **Test ID:** https://w3id.org/rsfc/test/RSFC-14-2
- **Result:** false
- **Process:** Searches for workflows that contain test or tests in their names
- **Evidence:** Could not find any workflows or actions that mention test in their names
- **Suggestions:** You should include github actions that run tests to ensure quality. More information at https://everse.software/RSQKit/task_automation_github_actions

<a id="repository_workflows-https---w3id-org-rsfc-test-rsfc-19-1"></a>
#### Repository has workflows

- **Test ID:** https://w3id.org/rsfc/test/RSFC-19-1
- **Result:** true
- **Process:** Searches for workflows in the repository
- **Evidence:** Workflows were found in:
	- https://raw.githubusercontent.com/oeg-upm/rsfc/main/.github/workflows/pypi-publish.yml
	- https://raw.githubusercontent.com/oeg-upm/rsfc/main/.github/workflows/use-rsfc.yml
	- https://raw.githubusercontent.com/oeg-upm/rsfc/main/.github/workflows/run-rsfc.yml
- **Suggestions:** No suggestions

### requirements_specified

<a id="requirements_specified-https---w3id-org-rsfc-test-rsfc-13-1"></a>
#### Dependencies are declared

- **Test ID:** https://w3id.org/rsfc/test/RSFC-13-1
- **Result:** true
- **Process:** Searches for dependencies in project configuration files, README and dependencies files such as requirements.txt
- **Evidence:** Requirements were found in:
	- https://raw.githubusercontent.com/oeg-upm/rsfc/main/requirements.txt
	- https://raw.githubusercontent.com/oeg-upm/rsfc/main/pyproject.toml
	- https://raw.githubusercontent.com/oeg-upm/rsfc/main/README.md
- **Suggestions:** No suggestions

<a id="requirements_specified-https---w3id-org-rsfc-test-rsfc-13-3"></a>
#### Dependencies have version numbers

- **Test ID:** https://w3id.org/rsfc/test/RSFC-13-3
- **Result:** false
- **Process:** Checks if all of the dependencies stated in the machine-readable file (e.g. requirements.txt, pyproject.toml, etc.) of the repository have a version indicated
- **Evidence:** One or more dependencies do not have a version stated
- **Suggestions:** All of your dependencies should have their versions stated to ensure its reproducibility. More information at https://everse.software/RSQKit/reproducible_software_environments

<a id="requirements_specified-https---w3id-org-rsfc-test-rsfc-13-4"></a>
#### There is a dependencies machine-readable file

- **Test ID:** https://w3id.org/rsfc/test/RSFC-13-4
- **Result:** true
- **Process:** Checks if dependencies are indicated in a machine-readable file
- **Evidence:** There is a machine-readable file for dependencies
- **Suggestions:** No suggestions

### software_has_citation

<a id="software_has_citation-https---w3id-org-rsfc-test-rsfc-12-1"></a>
#### There is an article citation or reference publication

- **Test ID:** https://w3id.org/rsfc/test/RSFC-12-1
- **Result:** false
- **Process:** Searches for an article citation or a reference publication in the codemeta and citation files
- **Evidence:** Could not find neither a reference publication or citation to an article in the repository
- **Suggestions:** You should include other forms of citation like article citations and reference publications in your software's metadata. More information at https://everse.software/RSQKit/creating_good_readme

<a id="software_has_citation-https---w3id-org-rsfc-test-rsfc-18-1"></a>
#### Repository has citation

- **Test ID:** https://w3id.org/rsfc/test/RSFC-18-1
- **Result:** true
- **Process:** Searches for a CITATION.cff file and README file in the repository
- **Evidence:** A citation was found in:
	- https://raw.githubusercontent.com/oeg-upm/rsfc/main/CITATION.cff
- **Suggestions:** No suggestions

### software_has_documentation

<a id="software_has_documentation-https---w3id-org-rsfc-test-rsfc-04-2"></a>
#### There is a README

- **Test ID:** https://w3id.org/rsfc/test/RSFC-04-2
- **Result:** true
- **Process:** Searches for a README file in the repository
- **Evidence:** There is a README file in the repository
- **Suggestions:** No suggestions

<a id="software_has_documentation-https---w3id-org-rsfc-test-rsfc-05-2"></a>
#### There is contact and/or support metadata

- **Test ID:** https://w3id.org/rsfc/test/RSFC-05-2
- **Result:** false
- **Process:** Searches for contact and support information in the repository
- **Evidence:** Could not find any of the following information: contact, support_channels
- **Suggestions:** You should include contact information in your software's metadata in case someone wants to ask for information.

<a id="software_has_documentation-https---w3id-org-rsfc-test-rsfc-05-3"></a>
#### Software documentation

- **Test ID:** https://w3id.org/rsfc/test/RSFC-05-3
- **Result:** true
- **Process:** Searches for a README file in the root repository and other forms of documentation such as a Read The Docs badge or url
- **Evidence:** Documentation was found in: 	
- https://raw.githubusercontent.com/oeg-upm/rsfc/main/README.md
- **Suggestions:** No suggest

<a id="software_has_documentation-https---w3id-org-rsfc-test-rsfc-13-2"></a>
#### There are installation instructions

- **Test ID:** https://w3id.org/rsfc/test/RSFC-13-2
- **Result:** true
- **Process:** Searches for installation instructions in the README file of the repository
- **Evidence:** Installation instructions were found in the repository
- **Suggestions:** No suggestions

### software_has_license

<a id="software_has_license-https---w3id-org-rsfc-test-rsfc-15-1"></a>
#### Software has license

- **Test ID:** https://w3id.org/rsfc/test/RSFC-15-1
- **Result:** true
- **Process:** Searches for a file named 'LICENSE' or 'LICENSE.md' in the root of the repository.
- **Evidence:** A license was found in:
	- https://raw.githubusercontent.com/oeg-upm/rsfc/main/codemeta.json
	- https://raw.githubusercontent.com/oeg-upm/rsfc/main/pyproject.toml
	- https://raw.githubusercontent.com/oeg-upm/rsfc/main/LICENSE
- **Suggestions:** No suggestions

<a id="software_has_license-https---w3id-org-rsfc-test-rsfc-15-2"></a>
#### License is SPDX compliant

- **Test ID:** https://w3id.org/rsfc/test/RSFC-15-2
- **Result:** false
- **Process:** Checks if the licenses detected are SPDX compliant
- **Evidence:** There is one or more licenses that are not SPDX compliant
- **Suggestions:** You should include SPDX tags to ensure that your licenses are machine-readable. More information at https://everse.software/RSQKit/licensing_software

<a id="software_has_license-https---w3id-org-rsfc-test-rsfc-16-1"></a>
#### License referenced in metadata files

- **Test ID:** https://w3id.org/rsfc/test/RSFC-16-1
- **Result:** true
- **Process:** Searches for licensing information in the codemeta, citation and package files if they exist
- **Evidence:** License information was found in metadata files
- **Suggestions:** No suggestions

### software_has_tests

<a id="software_has_tests-https---w3id-org-rsfc-test-rsfc-14-1"></a>
#### Presence of tests in repository

- **Test ID:** https://w3id.org/rsfc/test/RSFC-14-1
- **Result:** true
- **Process:** Searches for files and/or directories that mention test in their names
- **Evidence:** Files and/or directories that mention test were found at:	
- doc/test	
- doc/test/RSFC-01-1	
- doc/test/RSFC-01-1/RSFC-01-1.html	
- doc/test/RSFC-01-1/RSFC-01-1.jsonld	
- doc/test/RSFC-01-1/RSFC-01-1.ttl	
- doc/test/RSFC-01-2	
- doc/test/RSFC-01-2/RSFC-01-2.html	
- doc/test/RSFC-01-2/RSFC-01-2.jsonld	
- doc/test/RSFC-01-2/RSFC-01-2.ttl	
- doc/test/RSFC-01-3	
- doc/test/RSFC-01-3/RSFC-01-3.html	
- doc/test/RSFC-01-3/RSFC-01-3.jsonld	
- doc/test/RSFC-01-3/RSFC-01-3.ttl	
- doc/test/RSFC-03-1	
- doc/test/RSFC-03-1/RSFC-03-1.html	
- doc/test/RSFC-03-1/RSFC-03-1.jsonld	
- doc/test/RSFC-03-1/RSFC-03-1.ttl	
- doc/test/RSFC-03-2	
- doc/test/RSFC-03-2/RSFC-03-2.html	
- doc/test/RSFC-03-2/RSFC-03-2.jsonld	
- doc/test/RSFC-03-2/RSFC-03-2.ttl	
- doc/test/RSFC-03-3	
- doc/test/RSFC-03-3/RSFC-03-3.html	
- doc/test/RSFC-03-3/RSFC-03-3.jsonld	
- doc/test/RSFC-03-3/RSFC-03-3.ttl	
- doc/test/RSFC-03-4	
- doc/test/RSFC-03-4/RSFC-03-4.html	
- doc/test/RSFC-03-4/RSFC-03-4.jsonld	
- doc/test/RSFC-03-4/RSFC-03-4.ttl	
- doc/test/RSFC-03-5	
- doc/test/RSFC-03-5/RSFC-03-5.html	
- doc/test/RSFC-03-5/RSFC-03-5.jsonld	
- doc/test/RSFC-03-5/RSFC-03-5.ttl	
- doc/test/RSFC-03-6	
- doc/test/RSFC-03-6/RSFC-03-6.html	
- doc/test/RSFC-03-6/RSFC-03-6.jsonld	
- doc/test/RSFC-03-6/RSFC-03-6.ttl	
- doc/test/RSFC-04-1	
- doc/test/RSFC-04-1/RSFC-04-1.html	
- doc/test/RSFC-04-1/RSFC-04-1.jsonld	
- doc/test/RSFC-04-1/RSFC-04-1.ttl	
- doc/test/RSFC-04-2	
- doc/test/RSFC-04-2/RSFC-04-2.html	
- doc/test/RSFC-04-2/RSFC-04-2.jsonld	
- doc/test/RSFC-04-2/RSFC-04-2.ttl	
- doc/test/RSFC-04-3	
- doc/test/RSFC-04-3/RSFC-04-3.html	
- doc/test/RSFC-04-3/RSFC-04-3.jsonld	
- doc/test/RSFC-04-3/RSFC-04-3.ttl	
- doc/test/RSFC-04-4	
- doc/test/RSFC-04-4/RSFC-04-4.html	
- doc/test/RSFC-04-4/RSFC-04-4.jsonld	
- doc/test/RSFC-04-4/RSFC-04-4.ttl	
- doc/test/RSFC-04-5	
- doc/test/RSFC-04-5/RSFC-04-5.html	
- doc/test/RSFC-04-5/RSFC-04-5.jsonld	
- doc/test/RSFC-04-5/RSFC-04-5.ttl	
- doc/test/RSFC-05-1	
- doc/test/RSFC-05-1/RSFC-05-1.html	
- doc/test/RSFC-05-1/RSFC-05-1.jsonld	
- doc/test/RSFC-05-1/RSFC-05-1.ttl	
- doc/test/RSFC-05-2	
- doc/test/RSFC-05-2/RSFC-05-2.html	
- doc/test/RSFC-05-2/RSFC-05-2.jsonld	
- doc/test/RSFC-05-2/RSFC-05-2.ttl	
- doc/test/RSFC-05-3	
- doc/test/RSFC-05-3/RSFC-05-3.html	
- doc/test/RSFC-05-3/RSFC-05-3.jsonld	
- doc/test/RSFC-05-3/RSFC-05-3.ttl	
- doc/test/RSFC-06-1	
- doc/test/RSFC-06-1/RSFC-06-1.html	
- doc/test/RSFC-06-1/RSFC-06-1.jsonld	
- doc/test/RSFC-06-1/RSFC-06-1.ttl	
- doc/test/RSFC-06-2	
- doc/test/RSFC-06-2/RSFC-06-2.html	
- doc/test/RSFC-06-2/RSFC-06-2.jsonld	
- doc/test/RSFC-06-2/RSFC-06-2.ttl	
- doc/test/RSFC-06-3	
- doc/test/RSFC-06-3/RSFC-06-3.html	
- doc/test/RSFC-06-3/RSFC-06-3.jsonld	
- doc/test/RSFC-06-3/RSFC-06-3.ttl	
- doc/test/RSFC-06-4	
- doc/test/RSFC-06-4/RSFC-06-4.html	
- doc/test/RSFC-06-4/RSFC-06-4.jsonld	
- doc/test/RSFC-06-4/RSFC-06-4.ttl	
- doc/test/RSFC-07-1	
- doc/test/RSFC-07-1/RSFC-07-1.html	
- doc/test/RSFC-07-1/RSFC-07-1.jsonld	
- doc/test/RSFC-07-1/RSFC-07-1.ttl	
- doc/test/RSFC-07-2	
- doc/test/RSFC-07-2/RSFC-07-2.html	
- doc/test/RSFC-07-2/RSFC-07-2.jsonld	
- doc/test/RSFC-07-2/RSFC-07-2.ttl	
- doc/test/RSFC-08-1	
- doc/test/RSFC-08-1/RSFC-08-1.html	
- doc/test/RSFC-08-1/RSFC-08-1.jsonld	
- doc/test/RSFC-08-1/RSFC-08-1.ttl	
- doc/test/RSFC-09-1	
- doc/test/RSFC-09-1/RSFC-09-1.html	
- doc/test/RSFC-09-1/RSFC-09-1.jsonld	
- doc/test/RSFC-09-1/RSFC-09-1.ttl	
- doc/test/RSFC-12-1	
- doc/test/RSFC-12-1/RSFC-12-1.html	
- doc/test/RSFC-12-1/RSFC-12-1.jsonld	
- doc/test/RSFC-12-1/RSFC-12-1.ttl	
- doc/test/RSFC-13-1	
- doc/test/RSFC-13-1/RSFC-13-1.html	
- doc/test/RSFC-13-1/RSFC-13-1.jsonld	
- doc/test/RSFC-13-1/RSFC-13-1.ttl	
- doc/test/RSFC-13-2	
- doc/test/RSFC-13-2/RSFC-13-2.html	
- doc/test/RSFC-13-2/RSFC-13-2.jsonld	
- doc/test/RSFC-13-2/RSFC-13-2.ttl	
- doc/test/RSFC-13-3	
- doc/test/RSFC-13-3/RSFC-13-3.html	
- doc/test/RSFC-13-3/RSFC-13-3.jsonld	
- doc/test/RSFC-13-3/RSFC-13-3.ttl	
- doc/test/RSFC-13-4	
- doc/test/RSFC-13-4/RSFC-13-4.html	
- doc/test/RSFC-13-4/RSFC-13-4.jsonld	
- doc/test/RSFC-13-4/RSFC-13-4.ttl	
- doc/test/RSFC-14-1	
- doc/test/RSFC-14-1/RSFC-14-1.html	
- doc/test/RSFC-14-1/RSFC-14-1.jsonld	
- doc/test/RSFC-14-1/RSFC-14-1.ttl	
- doc/test/RSFC-14-2	
- doc/test/RSFC-14-2/RSFC-14-2.html	
- doc/test/RSFC-14-2/RSFC-14-2.jsonld	
- doc/test/RSFC-14-2/RSFC-14-2.ttl	
- doc/test/RSFC-15-1	
- doc/test/RSFC-15-1/RSFC-15-1.html	
- doc/test/RSFC-15-1/RSFC-15-1.jsonld	
- doc/test/RSFC-15-1/RSFC-15-1.ttl	
- doc/test/RSFC-15-2	
- doc/test/RSFC-15-2/RSFC-15-2.html	
- doc/test/RSFC-15-2/RSFC-15-2.jsonld	
- doc/test/RSFC-15-2/RSFC-15-2.ttl	
- doc/test/RSFC-16-1	
- doc/test/RSFC-16-1/RSFC-16-1.html	
- doc/test/RSFC-16-1/RSFC-16-1.jsonld	
- doc/test/RSFC-16-1/RSFC-16-1.ttl	
- doc/test/RSFC-17-1	
- doc/test/RSFC-17-1/RSFC-17-1.html	
- doc/test/RSFC-17-1/RSFC-17-1.jsonld	
- doc/test/RSFC-17-1/RSFC-17-1.ttl	
- doc/test/RSFC-17-2	
- doc/test/RSFC-17-2/RSFC-17-2.html	
- doc/test/RSFC-17-2/RSFC-17-2.jsonld	
- doc/test/RSFC-17-2/RSFC-17-2.ttl	
- doc/test/RSFC-17-3	
- doc/test/RSFC-17-3/RSFC-17-3.html	
- doc/test/RSFC-17-3/RSFC-17-3.jsonld	
- doc/test/RSFC-17-3/RSFC-17-3.ttl	
- doc/test/RSFC-18-1	
- doc/test/RSFC-18-1/RSFC-18-1.html	
- doc/test/RSFC-18-1/RSFC-18-1.jsonld	
- doc/test/RSFC-18-1/RSFC-18-1.ttl	
- doc/test/RSFC-19-1	
- doc/test/RSFC-19-1/RSFC-19-1.html	
- doc/test/RSFC-19-1/RSFC-19-1.jsonld	
- doc/test/RSFC-19-1/RSFC-19-1.ttl	
- doc/test/RSFC-20-1	
- doc/test/RSFC-20-1/RSFC-20-1.html	
- doc/test/RSFC-20-1/RSFC-20-1.jsonld	
- doc/test/RSFC-20-1/RSFC-20-1.ttl	
- doc/web_generation_scripts/templates/template_test.html	
- doc/web_generation_scripts/test_register.py	
- src/rsfc/rsfc_tests	
- src/rsfc/rsfc_tests/__init__.py	
- src/rsfc/rsfc_tests/rsfc_tests.py
- **Suggestions:** No suggestions

### support_issue_tracking

<a id="support_issue_tracking-https---w3id-org-rsfc-test-rsfc-20-1"></a>
#### Repository has an issue tracker

- **Test ID:** https://w3id.org/rsfc/test/RSFC-20-1
- **Result:** true
- **Process:** Checks if there is an issue tracker in the repository.
- **Evidence:** Found an issue tracker in the repository
- **Suggestions:** No suggestions

### version_control_use

<a id="version_control_use-https---w3id-org-rsfc-test-rsfc-05-1"></a>
#### There is a repostatus badge

- **Test ID:** https://w3id.org/rsfc/test/RSFC-05-1
- **Result:** true
- **Process:** Searches for a repo status badge in the README file of the repository
- **Evidence:** A repo status badge was found in the repository
- **Suggestions:** No suggestions

<a id="version_control_use-https---w3id-org-rsfc-test-rsfc-09-1"></a>
#### Repository is from Github/Gitlab

- **Test ID:** https://w3id.org/rsfc/test/RSFC-09-1
- **Result:** true
- **Process:** Checks if the URL provided is indeed a Github or Gitlab repository
- **Evidence:** URL provided is a Github or Gitlab repository
- **Suggestions:** No suggestions

<a id="version_control_use-https---w3id-org-rsfc-test-rsfc-17-1"></a>
#### Repository active

- **Test ID:** https://w3id.org/rsfc/test/RSFC-17-1
- **Result:** true
- **Process:** Checks if there is a repo_status badge with value Active and if there are commits in the repository
- **Evidence:** Repository is enabled and has commits
- **Suggestions:** No suggestions

<a id="version_control_use-https---w3id-org-rsfc-test-rsfc-17-2"></a>
#### Commit history

- **Test ID:** https://w3id.org/rsfc/test/RSFC-17-2
- **Result:** true
- **Process:** Checks if the software repository has a commits history
- **Evidence:** Commits were found in the repository
- **Suggestions:** No suggestions

<a id="version_control_use-https---w3id-org-rsfc-test-rsfc-17-3"></a>
#### Commits are linked to issues

- **Test ID:** https://w3id.org/rsfc/test/RSFC-17-3
- **Result:** true
- **Process:** Checks if there is at least one of the existing issues (opened or closed) referenced in any of the commits made in the default branch of the repository
- **Evidence:** There is at least one commit linked to an issue
- **Suggestions:** No suggestions

### versioning_standards_use

<a id="versioning_standards_use-https---w3id-org-rsfc-test-rsfc-03-3"></a>
#### Release versions follow a community established convention

- **Test ID:** https://w3id.org/rsfc/test/RSFC-03-3
- **Result:** true
- **Process:** Checks if all of the releases versions follow the SemVer or CalVer versioning standards
- **Evidence:** All of the releases follow a versioning standard
- **Suggestions:** No suggestions

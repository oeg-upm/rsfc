#Zenodo Regex

REGEX_ZENODO_BADGE = r'https://zenodo\.org/badge/latestdoi/\d+'
REGEX_DOI_URL = r'https://doi\.org/\S+'

#Software Heritage Regex

REGEX_SOFTWARE_HERITAGE_BADGE = r'https://archive\.softwareheritage\.org/badge/(origin|swh):[^\)\]\s]+'

#Issue reference Regex

REGEX_ISSUE_REF = r"(?:closes|fixes)\s*(?:issue\s*)?\(?#(\d+)\)?"


#Versioning Regex

REGEX_SEMVER = r'^\d+\.\d+\.\d+$'
REGEX_SEMVER_V = r'^v\d+\.\d+\.\d+$'
REGEX_SEMVER_PRERELEASE = r'^\d+\.\d+\.\d+-(alpha|beta|rc(\.\d+)?)$'
REGEX_SEMVER_BUILD_METADATA = r'^\d+\.\d+\.\d+\+[\w\.]+$'
REGEX_SEMVER_PRERELEASE_AND_BUILD = r'^\d+\.\d+\.\d+-(alpha|beta|rc(\.\d+)?)\+[\w\.]+$'

REGEX_CALVER_YYYY_MM_DD = r'^\d{4}\.(0[1-9]|1[0-2])\.(0[1-9]|[12][0-9]|3[01])$'
REGEX_CALVER_YYYY_MM = r'^\d{4}\.(0[1-9]|1[0-2])$'
REGEX_CALVER_YYYYMMDD = r'^\d{4}(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])$'
REGEX_CALVER_YY_MM = r'^\d{2}\.(0[1-9]|1[0-2])$'
REGEX_CALVER_YYYY_MM_DD_PRERELEASE = r'^\d{4}\.(0[1-9]|1[0-2])\.(0[1-9]|[12][0-9]|3[01])-(alpha|beta|rc(\.\d+)?)$'


#ID Schema Regex

DOI_SCHEMA_REGEX = r'^10\.\d{4,9}/[-._;()/:A-Z0-9]+$'
ORCID_SCHEMA_REGEX = r'^https?://orcid\.org/\d{4}-\d{4}-\d{4}-\d{3}[0-9X]$'
SWHID_SCHEMA_REGEX = r'^swh:1:[a-z]+:[0-9a-f]{40}$'
URN_SCHEMA_REGEX = r'^urn:[a-z0-9][a-z0-9-]{1,31}:[\w\-.:\/?#\[\]@!$&\'()*+,;=]+$'
GITHUB_SCHEMA_REGEX = r'^https?://github\.com/[^/]+/[^/]+/?$'
ZENODO_BADGE_REGEX = r'^https?://zenodo\.org/badge/latestdoi/\d+$'
DOI_URL_REGEX = r'^https?://doi\.org/10\.\d{4,9}/[-._;()/:A-Z0-9]+$'


#Processes

PROCESS_LICENSE = "Searches for a file named 'LICENSE' or 'LICENSE.md' in the root of the repository."
PROCESS_LICENSE_INFO_IN_METADATA_FILES = 'Searches for licensing information in the codemeta, citation and package files if they exist'
PROCESS_LICENSE_SPDX_COMPLIANT = 'Checks if the licenses detected are SPDX compliant'
PROCESS_CITATION = "Searches for a CITATION.cff file and README file in the repository"
PROCESS_REQUIREMENTS = "Searches for dependencies in project configuration files, README and dependencies files such as requirements.txt"
PROCESS_RELEASES = "Searches for release tags in the repository"
PROCESS_RELEASE_ID_VERSION = 'Checks if all of the releases have an identifier and a version'
PROCESS_SEMANTIC_VERSIONING = 'Checks if all of the releases versions follow the SemVer or CalVer versioning standards'
PROCESS_VERSION_SCHEME = 'Checks if all of the version identifiers follow the same scheme'
PROCESS_VERSION_CONTROL_USE = "Searches for commits and branches in the repository"
PROCESS_WORKFLOWS = "Searches for workflows in the repository"
PROCESS_IDENTIFIER = "Searches for an identifier (i.e. DOI or SWHID) in the README file of the repository"
PROCESS_DESCRIPTIVE_METADATA = "Searches for description, programming languages, date of creation and keywords in the repository"
PROCESS_README = 'Searches for a README file in the repository'
PROCESS_DOCUMENTATION = "Searches for a README file in the root repository and other forms of documentation such as a Read The Docs badge or url"
PROCESS_CONTACT_SUPPORT_DOCUMENTATION = 'Searches for contact and support information in the repository'
PROCESS_INSTALLATION = 'Searches for installation instructions in the README file of the repository'
PROCESS_DEPENDENCIES_VERSION = 'Checks if all of the dependencies stated in the machine-readable file (e.g. requirements.txt, pyproject.toml, etc.) of the repository have a version indicated'
PROCESS_DEPENDENCIES_MACHINE_READABLE_FILE = 'Checks if dependencies are indicated in a machine-readable file'
PROCESS_ID_PROPER_SCHEMA = 'Checks if the identifiers associated with the software follow any of these schemas: DOI, URN, GITHUB and SWHID'
PROCESS_ID_ASSOCIATED_WITH_SOFTWARE = 'Searches for an identifier in the CITATION.cff, codemeta.json and README files'
PROCESS_AUTOMATED_TESTS = 'Searches for workflows that contain test or tests in their names'
PROCESS_TESTS = 'Searches for files and/or directories that mention test in their names'
PROCESS_RELEASE_CONSISTENCY = 'Checks if the latest release tag matches the version stated in the package file of the repository'
PROCESS_METADATA_EXISTS = 'Searches for codemeta, citation and package files in the repository'
PROCESS_TITLE_DESCRIPTION = 'Checks if there is a title and a description for the software in the metadata'
PROCESS_CODEMETA = 'Searches for a codemeta.json file in the repository'
PROCESS_REPO_STATUS = 'Searches for a repo status badge in the README file of the repository'
PROCESS_REPO_ENABLED_AND_COMMITS = 'Checks if there is a repo_status badge with value Active and if there are commits in the repository'
PROCESS_TICKETS = 'Searches for tickets or issues in the repository'
PROCESS_REFERENCE_PUBLICATION = 'Searches for an article citation or a reference publication in the codemeta and citation files'
PROCESS_IS_GITHUB_OR_GITLAB_REPOSITORY = 'Checks if the URL provided is indeed a Github or Gitlab repository'
PROCESS_ZENODO_SOFTWARE_HERITAGE = 'Searches for Zenodo and Software Heritage badges in the README file of the repository'
PROCESS_IDENTIFIER_IN_README_CITATION = 'Searches for an identifier in the README or CITATION.cff files of the repository'
PROCESS_ID_RESOLVES_TO_SOFTWARE = 'Checks if the identifier found in the README file or metadata files (i.e. codemeta.json, CITATION.cff) resolves to a page that links back to the software repository'
PROCESS_AUTHORS = 'Searches for authors in various files of the repository (i.e. CITATION.cff, AUTHORS.md, codemeta.json)'
PROCESS_CONTRIBUTORS = "Searches for contributors in various files of the repository (i.e. codemeta.json, pyproject.toml, pom.xml)'"
PROCESS_AUTHOR_ORCIDS = 'Checks if all authors stated in the CITATION.cff file have an ORCID assigned'
PROCESS_AUTHOR_ROLES = 'Checks if all authors stated in a codemeta.json file have a role assigned '
PROCESS_VERSION_IN_METADATA = 'Checks if a version number for the software is indicated in the CITATION.cff, codemeta.json or package files(i.e. pyproject.toml, pom.xml, etc.)'
PROCESS_COMMITS_LINKED_TO_ISSUES = 'Checks if there is at least one of the existing issues (opened or closed) referenced in any of the commits made in the default branch of the repository'
PROCESS_COMMITS_HISTORY = 'Checks if the software repository has a commits history'
PROCESS_LICENSE_INFORMATION_PROVIDED = 'Checks if license information is found in the README file of the repository'
PROCESS_ISSUE_TRACKER = "Checks if there is an issue tracker in the repository."


#Evidences

EVIDENCE_LICENSE = 'A license was found in:'
EVIDENCE_CITATION = 'A citation was found in:'
EVIDENCE_COMMITS = 'Commits were found in the repository'
EVIDENCE_BRANCHES = 'Branches were found in the repository'
EVIDENCE_DOCUMENTATION = 'Documentation was found in: '
EVIDENCE_DOCUMENTATION_README = 'There is a README file in the repository'
EVIDENCE_DOCUMENTATION_ONLY_README = 'A README file was found in: '
EVIDENCE_DOCUMENTATION_ONLY_READTHEDOCS = 'A Read The Docs badge/url was found in: '
EVIDENCE_METADATA_CODEMETA = 'A codemeta.json file was found in the root of the repository'
EVIDENCE_DESCRIPTIVE_METADATA = 'Descriptive metadata was found in the repository'
EVIDENCE_RELEASES = 'These releases were found:'
EVIDENCE_DOI_IDENTIFIER = 'A valid DOI was found in:'
EVIDENCE_DOI_RESOLVES = 'All of the DOIs in the README file resolve'
EVIDENCE_WORKFLOWS = 'Workflows were found in:'
EVIDENCE_DEPENDENCIES = 'Requirements were found in:'
EVIDENCE_RELEASE_ID_AND_VERSION = 'All of the releases have an id and a version'
EVIDENCE_VERSIONING_STANDARD = 'All of the releases follow a versioning standard'
EVIDENCE_IDENTIFIER_SCHEME_COMPLIANT = 'All of the releases URLs follow the same scheme'
EVIDENCE_TITLE_AND_DESCRIPTION = 'Title and description were found in the repository'
EVIDENCE_REPO_STATUS = 'A repo status badge was found in the repository'
EVIDENCE_CONTACT_INFO = 'Contact and support information was found in the repository'
EVIDENCE_SPDX_COMPLIANT = 'Licenses are SPDX compliant'
EVIDENCE_LICENSE_INFO_IN_METADATA = 'License information was found in metadata files'
EVIDENCE_LICENSE_INFORMATION_PROVIDED = 'License information was found in the README file of the repository'
EVIDENCE_TICKETS = 'Tickets/Issues were found in the repository'
EVIDENCE_REPO_ENABLED_AND_HAS_COMMITS = 'Repository is enabled and has commits'
EVIDENCE_AUTHOR_ORCIDS_CODEMETA = 'All authors in the codemeta.json file have an orcid identifier'
EVIDENCE_AUTHOR_ORCIDS_CFF = 'All authors in the CITATION.cff file have an orcid identifier'
EVIDENCE_AUTHOR_ORCIDS_BOTH = 'All authors in both the codemeta.json and CITATION.cff files have an orcid identifier'
EVIDENCE_AUTHORS = 'Authors were found in the repository'
EVIDENCE_CONTRIBUTORS = "Contributors were found in the repository"
EVIDENCE_AUTHOR_ROLES = 'All authors defined in the codemeta file have roles assigned'
EVIDENCE_REFERENCE_PUBLICATION = 'A reference publication was found in the codemeta file of the repository'
EVIDENCE_CITATION_TO_ARTICLE = 'A citation to an article was found in the repository'
EVIDENCE_REFERENCE_PUBLICATION_AND_CITATION_TO_ARTICLE = 'Both a citation to an article and a reference publication were found in the repository'
EVIDENCE_IS_IN_GITHUB_OR_GITLAB = 'URL provided is a Github or Gitlab repository'
EVIDENCE_IDENTIFIER_IN_README = 'An identifier was found in the README file of the repository'
EVIDENCE_IDENTIFIER_IN_CITATION = 'An identifier was found in the CITATION.cff file of the repository'
EVIDENCE_IDENTIFIER_IN_README_AND_CITATION = 'An identifier was found in both the README and CITATION.cff files of the repository'
EVIDENCE_ZENODO_DOI = 'A Zenodo DOI identifier was found in the repository'
EVIDENCE_SOFTWARE_HERITAGE_BADGE = 'A Software Heritage badge was found in the repository'
EVIDENCE_ZENODO_DOI_AND_SOFTWARE_HERITAGE = 'A Zenodo DOI identifier and a Software Heritage badge were found in the repository'
EVIDENCE_INSTALLATION = 'Installation instructions were found in the repository'
EVIDENCE_DEPENDENCIES_VERSION = 'All of the dependencies have a version stated'
EVIDENCE_DEPENDENCIES_MACHINE_READABLE_FILE = 'There is a machine-readable file for dependencies'
EVIDENCE_ID_RESOLVES = "Found the identifier {id} in the README and it resolves"
EVIDENCE_ID_COMMON_SCHEMA = 'All of the identifiers detected follow a common schema'
EVIDENCE_ID_ASSOCIATED_WITH_SOFTWARE = 'There is an identifier in the CITATION, codemeta and README files'
EVIDENCE_AUTOMATED_TESTS = 'There are workflows or actions that perform automated tests'
EVIDENCE_TESTS = 'Files and/or directories that mention test were found at:'
EVIDENCE_RELEASE_CONSISTENCY = 'Latest release matches the latest version stated'
EVIDENCE_METADATA_EXISTS = 'Found codemeta, citation and package files in the repository'
EVIDENCE_VERSION_IN_METADATA = 'Found the software version in one of the specified files'
EVIDENCE_CONTRIBUTORS = 'Found contributors metadata in the codemeta or package files'
EVIDENCE_COMMITS_LINKED_TO_ISSUES = 'There is at least one commit linked to an issue'
EVIDENCE_DOI_LINKS_BACK_TO_REPO = "The landing page of the software's identifier links back to the software repository"
EVIDENCE_ISSUE_TRACKER = "Found an issue tracker in the repository"


EVIDENCE_NO_LICENSE = 'Could not find any license in the repository'
EVIDENCE_LICENSE_NOT_CLEAR = 'Could not recognize a license clearer enough to detect which one it is'
EVIDENCE_NO_DOI_IDENTIFIER = 'Could not find any DOI in the README file of the repository'
EVIDENCE_NO_IDENTIFIER_FOUND = 'Could not find any identifier in the repository'
EVIDENCE_NO_IDENTIFIER_FOUND_README = 'Could not find any identifier in the README file'
EVIDENCE_NO_RESOLVE_DOI_IDENTIFIER = 'DOI found but not resolvable'
EVIDENCE_NO_CITATION = 'Could not find any citation in the repository'
EVIDENCE_NO_WORKFLOWS = 'Could not find any workflows in the repository'
EVIDENCE_NO_DEPENDENCIES = 'Could not find any dependencies indicated in the repository'
EVIDENCE_NO_METADATA_CODEMETA = 'Could not find a codemeta.json file in the repository'
EVIDENCE_NO_DESCRIPTIVE_METADATA = 'Could not find any of the following metadata: '
EVIDENCE_NO_README_AND_READTHEDOCS = 'Could not find neither README file or Read The Docs badge'
EVIDENCE_NO_DOCUMENTATION_README = 'Could not find a README file in the repository'
EVIDENCE_NO_RELEASES = 'Could not find any releases in the repository'
EVIDENCE_NO_RELEASE_ID_AND_VERSION = 'There is one or many releases that do not have an id and a version'
EVIDENCE_NO_VERSIONING_STANDARD = 'There is one version number of a release that does not follow either SemVer or CalVer'
EVIDENCE_NO_IDENTIFIER_SCHEME_COMPLIANT = 'There is one or more releases URLs that do not follow the same scheme as the rest of the release\'s URLs'
EVIDENCE_NO_TITLE = 'Could not find a title for the project in the repository'
EVIDENCE_NO_DESCRIPTION = 'Could not find a description for the project in the repository'
EVIDENCE_NO_TITLE_AND_DESCRIPTION = 'Could not find neither title or description in the repository'
EVIDENCE_NO_REPO_STATUS = 'Could not find a repo status badge in the repository'
EVIDENCE_NO_CONTACT_INFO = 'Could not find any of the following information: '
EVIDENCE_NO_SPDX_COMPLIANT = 'There is one or more licenses that are not SPDX compliant'
EVIDENCE_NO_LICENSE_INFO_IN_METADATA = 'Could not find any licensing information in the following metadata files: '
EVIDENCE_NO_LICENSE_INFORMATION_PROVIDED = 'Could not find license information in the README file of the repository'
EVIDENCE_NO_TICKETS = 'Could not find tickets/issues in the repository'
EVIDENCE_NO_REPO_ENABLED = 'Repository is not enabled'
EVIDENCE_NO_COMMITS = 'Could not find any commits in the repository'
EVIDENCE_NO_CONTRIBUTORS = 'Found authors but could not find any contributors in the repository'
EVIDENCE_NO_AUTHORS = 'Could not find any authors in the repository'
EVIDENCE_NO_AUTHOR_ORCIDS = 'One or more authors do not have an ORCID assigned'
EVIDENCE_NO_AUTHORS_IN_CODEMETA = 'There are no authors defined in the codemeta file'
EVIDENCE_NO_ALL_AUTHOR_ROLES = 'There are one or more authors in the codemeta file that do not have roles assigned'
EVIDENCE_NO_VALID_JSON = 'Codemeta file is not valid'
EVIDENCE_NO_CODEMETA_FOUND = 'Could not find codemeta file'
EVIDENCE_NO_REFERENCE_PUBLICATION_OR_CITATION_TO_ARTICLE = 'Could not find neither a reference publication or citation to an article in the repository'
EVIDENCE_NO_RESOLVE_GITHUB_OR_GITLAB_URL = 'Github/Gitlab URL provided does not resolve'
EVIDENCE_NO_GITHUB_OR_GITLAB_URL = 'URL provided is not from Github or Gitlab'
EVIDENCE_NO_IDENTIFIER_IN_README_OR_CITATION = 'Could not find an identifier in neither of the README or CITATION files in the repository'
EVIDENCE_NO_ZENODO_DOI_OR_SOFTWARE_HERITAGE = 'Could not find neither a Zenodo DOI identifier or a Software Heritage badge in the repository'
EVIDENCE_NO_INSTALLATION = 'Could not find any installation instructions in the repository'
EVIDENCE_NO_DEPENDENCIES_VERSION = 'One or more dependencies do not have a version stated'
EVIDENCE_NO_DEPENDENCIES_MACHINE_READABLE_FILE = 'Could not find a machine-readable file for dependencies'
EVIDENCE_NO_ID_RESOLVE = 'Found the identifier {id} in the README but it does not resolve or is not resolvable'
EVIDENCE_ID_NOT_URL = 'Found the identifier {id} in the README but it is not an URL'
EVIDENCE_NO_ID_COMMON_SCHEMA = 'One or more of the detected identifiers do not follow a common schema'
EVIDENCE_NO_ID_ASSOCIATED_WITH_SOFTWARE = 'Could not find an identifier in any of the CITATION, codemeta or README files'
EVIDENCE_SOME_ID_ASSOCIATED_WITH_SOFTWARE = 'An identifier was found but could not find it in the following locations: '
EVIDENCE_NO_TESTS = 'Could not find any files or directories that mention test'
EVIDENCE_NO_AUTOMATED_TESTS = 'Could not find any workflows or actions that mention test in their names'
EVIDENCE_NO_RELEASE_CONSISTENCY = 'Latest release does not match the latest version stated'
EVIDENCE_NOT_ENOUGH_RELEASE_INFO = 'Could not get the necessary information to perform the test, it being releases and/or version in package file'
EVIDENCE_NO_METADATA_EXISTS = 'Could not find any of the following metadata files: '
EVIDENCE_NO_VERSION_IN_METADATA = 'Could not find a version number for the software in any of the specified files'
EVIDENCE_NOT_ENOUGH_ISSUES_COMMITS_INFO = 'Could not get the necessary information to perform the test, it being the commits record or repository issues'
EVIDENCE_NO_COMMITS_LINKED_TO_ISSUES = 'There is not any commits linked to any issues in the repository'
EVIDENCE_DOI_NO_LINK_BACK_TO_REPO = "The landing page of the software's identifier does not link back to the software repository"
EVIDENCE_NO_ISSUE_TRACKER = "Could not find an issue tracker in the repository"


#Suggestions

SUGGEST_NO_IDENTIFIER = "You should include a resolvable, unique and persistent identifier in your README file. More information at https://everse.software/RSQKit/software_identifiers"
SUGGEST_IDENTIFIER_NO_RESOLVE = "You should make sure that your identifier is resolvable and persistent. More information at https://everse.software/RSQKit/software_identifiers"
SUGGEST_IDENTIFIER_NOT_HTTP = "The repository your identifier resolves to should  use a standard communication protocol. More information at https://everse.software/RSQKit/software_identifiers"
SUGGEST_IDENTIFIER_SCHEME = "Your identifier should follow a common schema like URN, DOI or SWHID. More information at https://everse.software/RSQKit/software_identifiers"
SUGGEST_IDENTIFIER_ASSOCIATED = "Remember that identifiers should be included in other files aside from README like codemeta.json, CITATION.cff. More information at https://everse.software/RSQKit/software_identifiers"
SUGGEST_NO_IDENTIFIER_IN_README_OR_CITATION = "You should include your software's identifier in your README or CITATION.cff files. More information at "
SUGGEST_DOI_NO_LINK_BACK_TO_REPO = "Your software's identifier should resolve to a page that links back to itself."
SUGGEST_NO_TITLE_DESCRIPTION = "You should add a title and a description to your software's metadata. More information at https://everse.software/RSQKit/software_metadata"
SUGGEST_NO_DESCRIPTION = "Remember to add a description to your software's metadata. More information at https://everse.software/RSQKit/software_metadata"
SUGGEST_NO_TITLE = "A title would be of much help to describe your software. More information at https://everse.software/RSQKit/software_metadata"
SUGGEST_NO_DESCRIPTIVE_METADATA = "You should describe your software using metadata. More information at https://everse.software/RSQKit/software_metadata"
SUGGEST_NO_CODEMETA = "You should create a codemeta file to describe your software. More information at https://everse.software/RSQKit/software_metadata"
SUGGEST_NO_METADATA_FILES = "You should describe your software in metadata files. More information at https://everse.software/RSQKit/software_metadata"
SUGGEST_NO_VERSION_IN_METADATA = "You should include the version of your software in its metadata. More information at https://everse.software/RSQKit/software_metadata"
SUGGEST_NO_RELEASES = "You should often launch releases of your software that contain new updates. More information at https://everse.software/RSQKit/releasing_software"
SUGGEST_NO_VERSIONING_STANDARD = "You should use a versioning standard for all of your releases. More information at https://everse.software/RSQKit/releasing_software"
SUGGEST_NO_RELEASE_CONSISTENCY = "It is good practice to keep consistency between the version of your latest release and the version in your metadata files"
SUGGEST_NO_RELEASE_ID_AND_VERSION = "The releases that you launch should have an id and a version to describe them. More information at https://everse.software/RSQKit/releasing_software"
SUGGEST_NO_IDENTIFIER_SCHEME_COMPLIANT = "The identifiers or URLs of your releases should follow a common scheme. More information at https://everse.software/RSQKit/releasing_software"
SUGGEST_NO_REPO_STATUS = "You should include the state of your repository in the README file"
SUGGEST_NO_README_AND_READTHEDOCS = "Your software should be well documented via a README file or a Read the Docs page. More information at https://everse.software/RSQKit/software_documentation"
SUGGEST_NO_CONTACT_INFO = "You should include contact information in your software's metadata in case someone wants to ask for information."
SUGGEST_NO_AUTHORS = "Your software should document its authors. More information at https://everse.software/RSQKit/documenting_software_project"
SUGGEST_NO_CONTRIBUTORS = "Your software should also document its contributors if there are any. More information at https://everse.software/RSQKit/documenting_software_project"
SUGGEST_NO_AUTHOR_ORCIDS = "When documenting your software's authors, you should include their ORCIDs if possible."
SUGGEST_NO_ALL_AUTHOR_ROLES = "When documenting your software's authors, you should include their roles if possible."
SUGGEST_NO_AUTHORS_IN_CODEMETA = "You should include your software's authors metadata in the codemeta.json file. More information at https://everse.software/RSQKit/software_metadata"
SUGGEST_NO_LICENSE = "You should have your software under a public license. More information at https://everse.software/RSQKit/licensing_software"
SUGGEST_NO_LICENSE_INFO = "You should provide license information in your README file. More information at https://everse.software/RSQKit/licensing_software"
SUGGEST_NO_LICENSE_INFO_METADATA = "Information about your license should be present in other metadata files like codemeta.json, package files or CITATION. More information on https://everse.software/RSQKit/software_metadata"
SUGGEST_NO_LICENSE_SPDX = "You should include SPDX tags to ensure that your licenses are machine-readable. More information at https://everse.software/RSQKit/licensing_software"
SUGGEST_NO_CITATION = "You should include a citation so other people can citate your research software. More information at https://everse.software/RSQKit/citing_software"
SUGGEST_NO_REFPUB_OR_ARTICLE = "You should include other forms of citation like article citations and reference publications in your software's metadata. More information at https://everse.software/RSQKit/creating_good_readme"
SUGGEST_NO_WORKFLOWS = "Your software should include workflows to automate tasks. More information at https://everse.software/RSQKit/task_automation_github_actions"
SUGGEST_NO_TESTS = "Your software should include tests to prove its functionability. More information at https://everse.software/RSQKit/testing_software"
SUGGEST_NO_TEST_ACTIONS = "You should include github actions that run tests to ensure quality. More information at https://everse.software/RSQKit/task_automation_github_actions"
SUGGEST_NO_README = "You should include an informative README file in your repository. More information at https://everse.software/RSQKit/creating_good_readme"
SUGGEST_ARCHIVE_SOFTWARE = "You should archive your software not only in Github/Gitlab. More information at https://everse.software/RSQKit/archiving_software"
SUGGEST_NO_DEPENDENCIES = "You should have your dependencies stated somewhere to enable reproducibility. More information at https://everse.software/RSQKit/reproducible_software_environments"
SUGGEST_NO_MACHINE_READABLE_DEPENDENCIES = "You should have your dependencies stated in a machine-readable file. More information at https://everse.software/RSQKit/reproducible_software_environments"
SUGGEST_NO_INSTALL_INSTRUCTIONS = "You should include instructions to facilitate the use of your software. More information at https://everse.software/RSQKit/creating_good_readme"
SUGGEST_NO_DEPENDENCIES_VERSION = "All of your dependencies should have their versions stated to ensure its reproducibility. More information at https://everse.software/RSQKit/reproducible_software_environments"
SUGGEST_NO_COMMITS = "Remember to keep track of your changes making commits to your repository. More information at https://everse.software/RSQKit/using_version_control"
SUGGEST_NO_ISSUES_LINK_COMMITS = "It is good practice to indicate in your commits which issues you are targeting or solving"
SUGGEST_NO_ACTIVE_REPO = "You should keep your repository active and indicate it with a repostatus badge"
SUGGEST_NO_ISSUE_TRACKER = "You should have an issue tracker in your repository to help you manage your ideas, next steps and bugs to fix."
SUGGEST_NO_COMMITS_OR_ISSUES = "Don't forget to make commits of your source code to your git repository and issues to improve version control. More information at https://everse.software/RSQKit/using_version_control"



#RSFC test identifiers

RSFC_01_1_ID = "https://w3id.org/rsfc/test/RSFC-01-1"
RSFC_01_2_ID = "https://w3id.org/rsfc/test/RSFC-01-2"
RSFC_01_3_ID = "https://w3id.org/rsfc/test/RSFC-01-3"
RSFC_03_1_ID = "https://w3id.org/rsfc/test/RSFC-03-1"
RSFC_03_2_ID = "https://w3id.org/rsfc/test/RSFC-03-2"
RSFC_03_3_ID = "https://w3id.org/rsfc/test/RSFC-03-3"
RSFC_03_4_ID = "https://w3id.org/rsfc/test/RSFC-03-4"
RSFC_03_5_ID = "https://w3id.org/rsfc/test/RSFC-03-5"
RSFC_03_6_ID = "https://w3id.org/rsfc/test/RSFC-03-6"
RSFC_04_1_ID = "https://w3id.org/rsfc/test/RSFC-04-1"
RSFC_04_2_ID = "https://w3id.org/rsfc/test/RSFC-04-2"
RSFC_04_3_ID = "https://w3id.org/rsfc/test/RSFC-04-3"
RSFC_04_4_ID = "https://w3id.org/rsfc/test/RSFC-04-4"
RSFC_04_5_ID = "https://w3id.org/rsfc/test/RSFC-04-5"
RSFC_05_1_ID = "https://w3id.org/rsfc/test/RSFC-05-1"
RSFC_05_2_ID = "https://w3id.org/rsfc/test/RSFC-05-2"
RSFC_05_3_ID = "https://w3id.org/rsfc/test/RSFC-05-3"
RSFC_06_1_ID = "https://w3id.org/rsfc/test/RSFC-06-1"
RSFC_06_2_ID = "https://w3id.org/rsfc/test/RSFC-06-2"
RSFC_06_3_ID = "https://w3id.org/rsfc/test/RSFC-06-3"
RSFC_06_4_ID = "https://w3id.org/rsfc/test/RSFC-06-4"
RSFC_07_1_ID = "https://w3id.org/rsfc/test/RSFC-07-1"
RSFC_07_2_ID = "https://w3id.org/rsfc/test/RSFC-07-2"
RSFC_08_1_ID = "https://w3id.org/rsfc/test/RSFC-08-1"
RSFC_09_1_ID = "https://w3id.org/rsfc/test/RSFC-09-1"
RSFC_12_1_ID = "https://w3id.org/rsfc/test/RSFC-12-1"
RSFC_13_1_ID = "https://w3id.org/rsfc/test/RSFC-13-1"
RSFC_13_2_ID = "https://w3id.org/rsfc/test/RSFC-13-2"
RSFC_13_3_ID = "https://w3id.org/rsfc/test/RSFC-13-3"
RSFC_13_4_ID = "https://w3id.org/rsfc/test/RSFC-13-4"
RSFC_14_1_ID = "https://w3id.org/rsfc/test/RSFC-14-1"
RSFC_14_2_ID = "https://w3id.org/rsfc/test/RSFC-14-2"
RSFC_15_1_ID = "https://w3id.org/rsfc/test/RSFC-15-1"
RSFC_15_2_ID = "https://w3id.org/rsfc/test/RSFC-15-2"
RSFC_15_3_ID = "https://w3id.org/rsfc/test/RSFC-15-3"
RSFC_16_1_ID = "https://w3id.org/rsfc/test/RSFC-16-1"
RSFC_17_1_ID = "https://w3id.org/rsfc/test/RSFC-17-1"
RSFC_17_2_ID = "https://w3id.org/rsfc/test/RSFC-17-2"
RSFC_17_3_ID = "https://w3id.org/rsfc/test/RSFC-17-3"
RSFC_18_1_ID = "https://w3id.org/rsfc/test/RSFC-18-1"
RSFC_19_1_ID = "https://w3id.org/rsfc/test/RSFC-19-1"
RSFC_20_1_ID = "https://w3id.org/rsfc/test/RSFC-20-1"


#Short descriptions

DESC_RSFC_01_1 = "There is an identifier and it resolves"
DESC_RSFC_01_2 = "There is an identifier in the metadata files"
DESC_RSFC_01_3 = "There is an identifier and it follows a common schema"
DESC_RSFC_03_1 = "The software has releases"
DESC_RSFC_03_2 = "Releases have version and identifier"
DESC_RSFC_03_3 = "Release versions follow SemVer or CalVer"
DESC_RSFC_03_4 = "Release identifiers follow the same scheme"
DESC_RSFC_03_5 = "Last release version corresponds to version in package file"
DESC_RSFC_03_6 = "There is a version number stated in metadata files"
DESC_RSFC_04_1 = "Metadata files exist"
DESC_RSFC_04_2 = "There is a README file"
DESC_RSFC_04_3 = "Title and description are declared"
DESC_RSFC_04_4 = "There is descriptive metadata"
DESC_RSFC_04_5 = "There is a codemeta file"
DESC_RSFC_05_1 = "There is a repostatus badge in the README file"
DESC_RSFC_05_2 = "Contact and support metadata exists"
DESC_RSFC_05_3 = "Software documentation exists"
DESC_RSFC_06_1 = "Authors are declared"
DESC_RSFC_06_2 = "Contributors are declared"
DESC_RSFC_06_3 = "Authors have an ORCID assigned"
DESC_RSFC_06_4 = "Authors have their roles stated"
DESC_RSFC_07_1 = "There is an identifier in README or CITATION"
DESC_RSFC_07_2 = "Software identifier resolves and links back to software"
DESC_RSFC_08_1 = "Metadata record is found in SWHeritage or Zenodo"
DESC_RSFC_09_1 = "Repository is from Github or Gitlab"
DESC_RSFC_12_1 = "There is an article citation or reference publication"
DESC_RSFC_13_1 = "Dependencies are declared"
DESC_RSFC_13_2 = "There are installation instructions"
DESC_RSFC_13_3 = "Dependencies have version numbers"
DESC_RSFC_13_4 = "Dependencies are in a machine-readable format"
DESC_RSFC_14_1 = "Tests are provided"
DESC_RSFC_14_2 = "There are actions to automate tests"
DESC_RSFC_15_1 = "There is a license"
DESC_RSFC_15_2 = "License is in SPDX format"
DESC_RSFC_15_3 = "License information is provided"
DESC_RSFC_16_1 = "License is referenced in metadata files"
DESC_RSFC_17_1 = "The repository has an 'active' status"
DESC_RSFC_17_2 = "Repository has a commit history"
DESC_RSFC_17_3 = "Commits are linked to issues"
DESC_RSFC_18_1 = "There are citations"
DESC_RSFC_19_1 = "Repository has continuous integration workflows"
DESC_RSFC_20_1 = "Repository has an issue tracker"


TEST_DESC_DICT = {
    "RSFC-01-1": DESC_RSFC_01_1,
    "RSFC-01-2": DESC_RSFC_01_2,
    "RSFC-01-3": DESC_RSFC_01_3,
    "RSFC-03-1": DESC_RSFC_03_1,
    "RSFC-03-2": DESC_RSFC_03_2,
    "RSFC-03-3": DESC_RSFC_03_3,
    "RSFC-03-4": DESC_RSFC_03_4,
    "RSFC-03-5": DESC_RSFC_03_5,
    "RSFC-03-6": DESC_RSFC_03_6,
    "RSFC-04-1": DESC_RSFC_04_1,
    "RSFC-04-2": DESC_RSFC_04_2,
    "RSFC-04-3": DESC_RSFC_04_3,
    "RSFC-04-4": DESC_RSFC_04_4,
    "RSFC-04-5": DESC_RSFC_04_5,
    "RSFC-05-1": DESC_RSFC_05_1,
    "RSFC-05-2": DESC_RSFC_05_2,
    "RSFC-05-3": DESC_RSFC_05_3,
    "RSFC-06-1": DESC_RSFC_06_1,
    "RSFC-06-2": DESC_RSFC_06_2,
    "RSFC-06-3": DESC_RSFC_06_3,
    "RSFC-06-4": DESC_RSFC_06_4,
    "RSFC-07-1": DESC_RSFC_07_1,
    "RSFC-07-2": DESC_RSFC_07_2,
    "RSFC-08-1": DESC_RSFC_08_1,
    "RSFC-09-1": DESC_RSFC_09_1,
    "RSFC-12-1": DESC_RSFC_12_1,
    "RSFC-13-1": DESC_RSFC_13_1,
    "RSFC-13-2": DESC_RSFC_13_2,
    "RSFC-13-3": DESC_RSFC_13_3,
    "RSFC-13-4": DESC_RSFC_13_4,
    "RSFC-14-1": DESC_RSFC_14_1,
    "RSFC-14-2": DESC_RSFC_14_2,
    "RSFC-15-1": DESC_RSFC_15_1,
    "RSFC-15-2": DESC_RSFC_15_2,
    "RSFC-15-3": DESC_RSFC_15_3,
    "RSFC-16-1": DESC_RSFC_16_1,
    "RSFC-17-1": DESC_RSFC_17_1,
    "RSFC-17-2": DESC_RSFC_17_2,
    "RSFC-17-3": DESC_RSFC_17_3,
    "RSFC-18-1": DESC_RSFC_18_1,
    "RSFC-19-1": DESC_RSFC_19_1,
    "RSFC-20-1": DESC_RSFC_20_1
}


#Dictionaries

INDICATORS_DICT = {
    'software_has_license': 'https://w3id.org/everse/i/indicators/software_has_license',
    'software_has_citation': 'https://w3id.org/everse/i/indicators/software_has_citation',
    'dependency_management': 'https://w3id.org/everse/i/indicators/dependency_management',
    'has_releases': 'https://w3id.org/everse/i/indicators/has_releases',
    'repository_workflows': 'https://w3id.org/everse/i/indicators/repository_workflows',
    'software_has_tests': 'https://w3id.org/everse/i/indicators/software_has_tests',
    'version_control_use': 'https://w3id.org/everse/i/indicators/version_control_use',
    'requirements_specified': 'https://w3id.org/everse/i/indicators/requirements_specified',
    'software_has_documentation': 'https://w3id.org/everse/i/indicators/software_has_documentation',
    'persistent_and_unique_identifier': 'https://w3id.org/everse/i/indicators/persistent_and_unique_identifier',
    'descriptive_metadata': 'https://w3id.org/everse/i/indicators/descriptive_metadata',
    'versioning_standards_use': 'https://w3id.org/everse/i/indicators/versioning_standards_use',
    'archived_in_software_heritage': 'https://w3id.org/everse/i/indicators/archived_in_software_heritage',
    'support_issue_tracking': 'https://w3id.org/everse/i/indicators/support_issue_tracking'
}

CHECKERS_DICT = {
    'rsfc' : {
        'name' : 'RSFC',
        'id' : 'https://w3id.org/rsfc/',
        'version' : '0.1.2'
    }
}


REPO_TYPES = {
    0: 'GITHUB',
    1: 'GITLAB'
}


SPDX_LICENSE_WHITELIST = [
    "MIT",
    "Apache-2.0",
    "BSD-2-Clause",
    "BSD-3-Clause",
    "GPL-2.0-only",
    "GPL-2.0-or-later",
    "GPL-3.0-only",
    "GPL-3.0-or-later",
    "LGPL-2.1-only",
    "LGPL-2.1-or-later",
    "LGPL-3.0-only",
    "LGPL-3.0-or-later",
    "MPL-2.0",
    "EPL-1.0",
    "EPL-2.0",
    "CDDL-1.0",
    "CC0-1.0",
    "Unlicense",
    "Artistic-2.0",
    "AGPL-3.0-only",
    "AGPL-3.0-or-later"
]


VERSIONING_REGEX_LIST = [
    REGEX_SEMVER,
    REGEX_SEMVER_V,
    REGEX_SEMVER_PRERELEASE,
    REGEX_SEMVER_BUILD_METADATA,
    REGEX_SEMVER_PRERELEASE_AND_BUILD,
    REGEX_CALVER_YYYY_MM_DD,
    REGEX_CALVER_YYYY_MM,
    REGEX_CALVER_YY_MM,
    REGEX_CALVER_YYYYMMDD,
    REGEX_CALVER_YYYY_MM_DD_PRERELEASE
]


ID_SCHEMA_REGEX_LIST = [
    DOI_SCHEMA_REGEX,
    SWHID_SCHEMA_REGEX,
    URN_SCHEMA_REGEX,
    GITHUB_SCHEMA_REGEX,
    ZENODO_BADGE_REGEX,
    DOI_URL_REGEX
]
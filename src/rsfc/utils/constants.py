#Zenodo Regex

REGEX_ZENODO_BADGE = r'https://zenodo\.org/badge/latestdoi/\d+'
REGEX_DOI_URL = r'https://doi\.org/\S+'

#Software Heritage Regex

REGEX_SOFTWARE_HERITAGE_BADGE = r'https://archive\.softwareheritage\.org/badge/(origin|swh):[^\)\]\s]+'


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
PROCESS_IDENTIFIER = "Searches for a DOI in the README file of the repository"
PROCESS_DESCRIPTIVE_METADATA = "Searches for description, programming languages, date of creation and keywords in the repository"
PROCESS_README = 'Searches for a README file in the repository'
PROCESS_DOCUMENTATION = "Searches for a README file in the root repository and other forms of documentation such as a Read The Docs badge or url"
PROCESS_CONTACT_SUPPORT_DOCUMENTATION = 'Searches for contact and support information in the repository'
PROCESS_INSTALLATION = 'Searches for installation instructions in the README file of the repository'
PROCESS_DEPENDENCIES_VERSION = 'Checks if all of the dependencies stated in the machine-readable file (e.g. requirements.txt, pyproject.toml, etc.) of the repository have a version indicated'
PROCESS_DEPENDENCIES_MACHINE_READABLE_FILE = 'Checks if dependencies are indicated in a machine-readable file'
PROCESS_ID_PROPER_SCHEMA = 'Checks if the identifiers associated with the software follow any of these schemas: DOI, ORCID, URN, GITHUB and SWHID'
PROCESS_ID_ASSOCIATED_WITH_SOFTWARE = 'Searches for an identifier in CITATION.cff, codemeta.json and README files'
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
PROCESS_ID_RESOLVES_TO_SOFTWARE = 'Checks if the identifier found in the README file of the repository resolves to the software'
PROCESS_AUTHORS_AND_CONTRIBS = 'Searches for authors and contributors in the varios files of the repository (e.g. CITATION.cff, AUTHORS.md, codemeta.json)'
PROCESS_AUTHOR_ORCIDS = 'Checks if all authors stated in the CITATION.cff file have an ORCID assigned'
PROCESS_AUTHOR_ROLES = 'Checks if all authors stated in a codemeta.json file have a role assigned '




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
EVIDENCE_VERSION_SCHEME_COMPLIANT = 'All of the releases URLs follow the same scheme'
EVIDENCE_TITLE_AND_DESCRIPTION = 'Title and description were found in the repository'
EVIDENCE_REPO_STATUS = 'A repo status badge was found in the repository'
EVIDENCE_CONTACT_INFO = 'Contact and support information was found in the repository'
EVIDENCE_SPDX_COMPLIANT = 'Licenses are SPDX compliant'
EVIDENCE_LICENSE_INFO_IN_METADATA = 'License information was found in metadata files'
EVIDENCE_TICKETS = 'Tickets/Issues were found in the repository'
EVIDENCE_REPO_ENABLED_AND_HAS_COMMITS = 'Repository is enabled and has commits'
EVIDENCE_AUTHOR_ORCIDS = 'All authors have ORCIDs'
EVIDENCE_AUTHORS_AND_CONTRIBUTORS = 'Authors and contributors were found in the repository'
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
EVIDENCE_ID_RESOLVES = 'There is an identifier and resolves'
EVIDENCE_ID_PROPER_SCHEMA = 'All of the identifiers detected follow a proper schema'
EVIDENCE_ID_ASSOCIATED_WITH_SOFTWARE = 'There is an identifier in the CITATION, codemeta and README'
EVIDENCE_AUTOMATED_TESTS = 'There are workflows or actions that perform automated tests'
EVIDENCE_TESTS = 'Files and/or directories that mention test were found at:'
EVIDENCE_RELEASE_CONSISTENCY = 'Latest release matches the latest version stated'
EVIDENCE_METADATA_EXISTS = 'Found codemeta, citation and package files in the repository'


EVIDENCE_NO_LICENSE = 'Could not find any license in the repository'
EVIDENCE_LICENSE_NOT_CLEAR = 'Could not recognize a license clearer enough to detect which one it is'
EVIDENCE_NO_DOI_IDENTIFIER = 'Could not find any DOI in the README file of the repository'
EVIDENCE_NO_IDENTIFIER_FOUND = 'Could not find any identifier in the repository'
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
EVIDENCE_NO_VERSION_SCHEME_COMPLIANT = 'There is one or more releases URLs that do not follow the same scheme as the rest of the release\'s URLs'
EVIDENCE_NO_TITLE = 'Could not find a title for the project in the repository'
EVIDENCE_NO_DESCRIPTION = 'Could not find a description for the project in the repository'
EVIDENCE_NO_TITLE_AND_DESCRIPTION = 'Could not find neither title or description in the repository'
EVIDENCE_NO_REPO_STATUS = 'Could not find a repo status badge in the repository'
EVIDENCE_NO_CONTACT_INFO = 'Could not find any of the following information: '
EVIDENCE_NO_SPDX_COMPLIANT = 'There is one or more licenses that are not SPDX compliant'
EVIDENCE_NO_LICENSE_INFO_IN_METADATA = 'Could not find any licensing information in the following metadata files: '
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
EVIDENCE_NO_ID_RESOLVE = 'There is an identifier but it does not resolve or is not resolvable'
EVIDENCE_ID_NOT_URL = 'There is an identifier but it is not an URL'
EVIDENCE_NO_ID_PROPER_SCHEMA = 'One or more of the detected identifiers do not follow a proper schema'
EVIDENCE_NO_ID_ASSOCIATED_WITH_SOFTWARE = 'Could not find an identifier in any of the locations checked'
EVIDENCE_SOME_ID_ASSOCIATED_WITH_SOFTWARE = 'An identifier was found but could not find it in the following locations: '
EVIDENCE_NO_TESTS = 'Could not find any files or directories that mention test'
EVIDENCE_NO_AUTOMATED_TESTS = 'Could not find any workflows or actions that mention test in their names'
EVIDENCE_NO_RELEASE_CONSISTENCY = 'Latest release does not match the latest version stated'
EVIDENCE_NOT_ENOUGH_RELEASE_INFO = 'Could not get the necessary information to perform the test, it being releases and/or version in package file'
EVIDENCE_NO_METADATA_EXISTS = 'Could not find any of the following metadata files: '


#Dictionaries

INDICATORS_DICT = {
    'software_has_license': 'https://w3id.org/everse/i/indicators/software_has_license',
    'software_has_citation': 'https://w3id.org/everse/i/indicators/software_has_citation',
    'dependency_management': 'https://w3id.org/everse/i/indicators/dependency_management',
    'has_releases': 'https://w3id.org/everse/i/indicators/has_releases',
    'repository_workflows': 'https://w3id.org/everse/i/indicators/repository_workflows',
    'software_tests': 'https://w3id.org/everse/i/indicators/software_tests',
    'version_control_use': 'https://w3id.org/everse/i/indicators/version_control_use',
    'requirements_specified': 'https://w3id.org/everse/i/indicators/requirements_specified',
    'software_documentation': 'https://w3id.org/everse/i/indicators/software_documentation',
    'persistent_and_unique_identifier': 'https://w3id.org/everse/i/indicators/persistent_and_unique_identifier',
    'descriptive_metadata': 'https://w3id.org/everse/i/indicators/descriptive_metadata',
    'semantic_versioning': 'https://w3id.org/everse/i/indicators/semantic_versioning',
    'archived_in_software_heritage': 'https://w3id.org/everse/i/indicators/archived_in_software_heritage'
}

CHECKERS_DICT = {
    'rsfc' : {
        'name' : 'RSFC',
        'id' : 'https://github.com/oeg-upm/rsfc',
        'version' : '0.0.1'
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
    ORCID_SCHEMA_REGEX,
    SWHID_SCHEMA_REGEX,
    URN_SCHEMA_REGEX,
    GITHUB_SCHEMA_REGEX,
    ZENODO_BADGE_REGEX
]
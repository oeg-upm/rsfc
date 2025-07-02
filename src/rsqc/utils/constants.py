#Regex

REGEX_ZENODO_BADGE = r'https://zenodo\.org/badge/latestdoi/\d+'
REGEX_ZENODO_URL = r'https://doi\.org/\S+'

#Processes

PROCESS_LICENSE = "Searches for a file named 'LICENSE' or 'LICENSE.md' in the root of the repository."
PROCESS_CITATION = "Searches for a .cff file in the repository and README file"
PROCESS_REQUIREMENTS = "Searches for dependencies in project configuration files, README and dependencies files such as requirements.txt"
PROCESS_RELEASES = "Searches for release tags in the repository"
PROCESS_VERSION_CONTROL_USE = "Searches for commits and branches in the repository"
PROCESS_WORKFLOWS = "Searches for workflows in the repository"
PROCESS_IDENTIFIER = "Searches for a DOI in the README file of the repository"
PROCESS_METADATA = "Searches for a codemeta.json file in the root of the repository"
PROCESS_DOCUMENTATION = "Searches for a README file in the root repository and other forms of documentation such as a Read The Docs badge or url"

#Evidences

EVIDENCE_LICENSE = 'A license was found in:'
EVIDENCE_CITATION = 'A citation was found in:'
EVIDENCE_COMMITS = 'Commits were found in the repository'
EVIDENCE_BRANCHES = 'Branches were found in the repository'
EVIDENCE_DOCUMENTATION = 'Documentation was found in:'
EVIDENCE_DOCUMENTATION_ONLY_README = 'A README file was found in: \nbut could not find a Read The Docs badge/url'
EVIDENCE_DOCUMENTATION_ONLY_READTHEDOCS = 'A Read The Docs badge/url was found in: \nbut could not find a README file'
EVIDENCE_METADATA_CODEMETA = 'A codemeta.json file was found in the root of the repository'
EVIDENCE_RELEASES = 'These releases were found:'
EVIDENCE_DOI_IDENTIFIER = 'A valid DOI was found in:'
EVIDENCE_WORKFLOWS = 'Workflows were found in:'
EVIDENCE_DEPENDENCIES = 'Requirements were found in:'

EVIDENCE_NO_LICENSE = 'Could not find any license in the repository'
EVIDENCE_NO_DOI_IDENTIFIER = 'Could not find any DOI in the README file of the repository'
EVIDENCE_NO_RESOLVE_DOI_IDENTIFIER = 'DOI found but not resolvable'
EVIDENCE_NO_CITATION = 'Could not find any citation in the repository'
EVIDENCE_NO_WORKFLOWS = 'Could not find any workflows in the repository'
EVIDENCE_NO_DEPENDENCIES = 'Could not find any dependencies indicated in the repository'
EVIDENCE_NO_METADATA_CODEMETA = 'Could not find a codemeta.json file in the repository'
EVIDENCE_NO_README_AND_READTHEDOCS = 'Could not find neither README file or Read The Docs badge'
EVIDENCE_NO_RELEASES = 'Could not find any releases in the repository'

#Dictionaries

INDICATORS_DICT = {
    'software_has_license' : 'https://w3id.org/everse/i/indicators/software_has_license',
    'software_has_citation' : 'https://w3id.org/everse/i/indicators/software_has_citation',
    'dependency_management' : 'https://w3id.org/everse/i/indicators/dependency_management',
    'has_releases' : 'https://w3id.org/everse/i/indicators/has_releases',
    'repository_workflows' : 'https://w3id.org/everse/i/indicators/repository_workflows',
    'software_tests' : 'https://w3id.org/everse/i/indicators/software_tests',
    'version_control_use' : 'https://w3id.org/everse/i/indicators/version_control_use',
    'requirements_specified' : 'https://w3id.org/everse/i/indicators/requirements_specified',
    'software_documentation' : 'https://w3id.org/everse/i/indicators/software_documentation',
    'persistent_and_unique_identifier' : 'https://w3id.org/everse/i/indicators/persistent_and_unique_identifier',
    'descriptive_metadata' : 'https://w3id.org/everse/i/indicators/descriptive_metadata'
}

CHECKERS_DICT = {
    'rsqc' : {
        'name' : 'RSQC',
        'id' : 'https://github.com/andriumon/rsqc',
        'version' : '0.0.1'
    }
}
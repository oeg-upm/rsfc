from rsfc.utils import constants
from rsfc.model import check as ch
import regex as re
import requests
from rsfc.utils import rsfc_helpers


################################################### FRSM_01 ###################################################

def test_id_presence_and_resolves(somef_data):
    if 'identifier' in somef_data:
        for item in somef_data['identifier']:
            if item['source']:
                if 'README' in item['source']:
                    id = item['result']['value']
                    
                    if id.startswith('http://') or id.startswith('https://'):
                        try:
                            response = requests.head(id, allow_redirects=True, timeout=10)
                            if response.status_code == 200:
                                output = "true"
                                evidence = constants.EVIDENCE_ID_RESOLVES
                            else:
                                output = "false"
                                evidence = constants.EVIDENCE_NO_ID_RESOLVE
                        except requests.RequestException:
                            output = "false"
                            evidence = None
                    else:
                        output = "false"
                        evidence = constants.EVIDENCE_ID_NOT_URL
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_IDENTIFIER_FOUND
                        
    
    check = ch.Check(constants.INDICATORS_DICT['persistent_and_unique_identifier'], 'RSFC-01-1', constants.PROCESS_IDENTIFIER, output, evidence)
    
    return check.convert()


def test_id_common_schema(somef_data):
    if 'identifier' in somef_data:
        compiled_patterns = []
        for pattern in constants.ID_SCHEMA_REGEX_LIST:
            compiled = re.compile(pattern)
            compiled_patterns.append(compiled)
            
        output = "true"
        evidence = constants.EVIDENCE_ID_COMMON_SCHEMA
            
        for item in somef_data['identifier']:
            if item['source']:
                if 'README' in item['source']:
                    if not any(pattern.match(item['result']['value']) for pattern in compiled_patterns):
                        output = "false"
                        evidence = constants.EVIDENCE_NO_ID_COMMON_SCHEMA
                        break
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_IDENTIFIER_FOUND_README
        
    
    check = ch.Check(constants.INDICATORS_DICT['persistent_and_unique_identifier'], 'RSFC-01-3', constants.PROCESS_ID_PROPER_SCHEMA, output, evidence)
    
    return check.convert()


def test_id_associated_with_software(somef_data, codemeta_data, cff_data):
    
    id_locations = {
        'codemeta': False,
        'cff': False,
        'readme': False
    }
    
    if codemeta_data != None and codemeta_data["identifier"] != None:
        id_locations["codemeta"] = True
        
    if cff_data != None and cff_data["identifiers"] != None:
        id_locations["cff"] = True

    if 'identifier' in somef_data:
        for item in somef_data['identifier']:
            if item['source']:
                if 'README' in item['source']:
                    id_locations['readme'] = True
        
        
    if any(id_locations.values()):
        output = "true"
        evidence = constants.EVIDENCE_SOME_ID_ASSOCIATED_WITH_SOFTWARE
        
        existing_id_locations = [key for key, value in id_locations.items() if value]
        existing_id_locations_txt = ', '.join(existing_id_locations)
        
        evidence += existing_id_locations_txt
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_ID_ASSOCIATED_WITH_SOFTWARE
    

    check = ch.Check(constants.INDICATORS_DICT['persistent_and_unique_identifier'], 'RSFC-01-2', constants.PROCESS_ID_ASSOCIATED_WITH_SOFTWARE, output, evidence)
    
    return check.convert()



################################################### FRSM_03 ###################################################


def test_version_number_in_metadata(somef_data, codemeta_data, cff_data):
    
    cff = False
    codemeta = False
    somef = False
    
    if cff_data != None and cff_data['version'] != None:
        cff = True
        
    if codemeta_data != None and codemeta_data['version'] != None:
        codemeta = True
        
    if 'version' in somef_data:
        somef = True
        
    if cff or codemeta or somef:
        output = "true"
        evidence = constants.EVIDENCE_VERSION_IN_METADATA
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_VERSION_IN_METADATA
        
    check = ch.Check(constants.INDICATORS_DICT['descriptive_metadata'], 'RSFC-03-6', constants.PROCESS_VERSION_IN_METADATA, output, evidence)

    return check.convert()


def test_has_releases(somef_data):
    if 'releases' not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_RELEASES
    else:
        output = "true"
        evidence = constants.EVIDENCE_RELEASES
        for item in somef_data['releases']:
            if 'type' in item['result']:
                if item['result']['type'] == 'Release':
                    if 'name' in item['result']:
                        evidence += f'\n\t- {item["result"]["name"]}'
                    elif 'tag' in item['result']:
                        evidence += f'\n\t- {item["result"]["tag"]}'
                    else:
                        evidence += f'\n\t- {item["result"]["url"]}'
                        
    check = ch.Check(constants.INDICATORS_DICT['has_releases'], 'RSFC-03-1', constants.PROCESS_RELEASES, output, evidence)

    return check.convert()
    
    
def test_release_id_and_version(somef_data):
    if 'releases' not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_RELEASES
    else:
        results = somef_data['releases']
        for item in results:
            if item['result']['url'] and item['result']['tag']:
                output = "true"
                evidence = constants.EVIDENCE_RELEASE_ID_AND_VERSION
            else:
                output = "false"
                evidence = constants.EVIDENCE_NO_RELEASE_ID_AND_VERSION
                break
                
    check = ch.Check(constants.INDICATORS_DICT['has_releases'], 'RSFC-03-2', constants.PROCESS_RELEASE_ID_VERSION, output, evidence)
    
    return check.convert()


def test_semantic_versioning_standard(somef_data):
    
    if 'releases' not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_RELEASES
    else:
        compiled_patterns = []
        for pattern in constants.VERSIONING_REGEX_LIST:
            compiled = re.compile(pattern)
            compiled_patterns.append(compiled)
            
        results = somef_data['releases']
        for item in results:
            if item['result']['tag']:
                if any(pattern.match(item['result']['tag']) for pattern in compiled_patterns):
                    output = "true"
                else:
                    output = "false"
                    evidence = constants.EVIDENCE_NO_VERSIONING_STANDARD
                    break
        
        if output == "true":
            evidence = constants.EVIDENCE_VERSIONING_STANDARD
                
    check = ch.Check(constants.INDICATORS_DICT['versioning_standards_use'], 'RSFC-03-3', constants.PROCESS_SEMANTIC_VERSIONING, output, evidence)
    
    return check.convert()
        
    
def test_version_scheme(somef_data):
    if 'releases' not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_RELEASES
    else:
        scheme = ''
        results = somef_data['releases']
        for item in results:
            if item['result']['url']:
                url = item['result']['url']
                if not scheme:
                    scheme = rsfc_helpers.build_url_pattern(url)
                if not scheme.match(url):
                    output = "false"
                    evidence = constants.EVIDENCE_NO_VERSION_SCHEME_COMPLIANT
                else:
                    output = "true"
                    
        if output == "true":
            evidence = constants.EVIDENCE_VERSION_SCHEME_COMPLIANT
        
    check = ch.Check(constants.INDICATORS_DICT['has_releases'], 'RSFC-03-4', constants.PROCESS_VERSION_SCHEME, output, evidence)
    
    return check.convert()



def test_latest_release_consistency(somef_data):
    latest_release = None
    version = None
    
    if 'releases' in somef_data:
        latest_release = rsfc_helpers.get_latest_release(somef_data)
        
    if 'version' in somef_data:
        version_data = somef_data['version'][0]['result']
        version = version_data.get('tag') or version_data.get('value')
    
    if version == None or latest_release == None:
        output = "error"
        evidence = constants.EVIDENCE_NOT_ENOUGH_RELEASE_INFO
    elif version == latest_release:
        output = "true"
        evidence = constants.EVIDENCE_RELEASE_CONSISTENCY
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_RELEASE_CONSISTENCY
        
        
    check = ch.Check(constants.INDICATORS_DICT['has_releases'], 'RSFC-03-5', constants.PROCESS_RELEASE_CONSISTENCY, output, evidence)
    
    return check.convert()

################################################### FRSM_04 ###################################################

def test_metadata_exists(somef_data, codemeta_data, cff_data):
    
    metadata_files = {
        'cff': False,
        'codemeta': False,
        'package_file': False
    }
    
    if cff_data != None:
        metadata_files['cff'] = True
        
    if codemeta_data != None:
        metadata_files['codemeta'] = True
        
    if 'has_package_file' in somef_data:
        metadata_files['package_file'] = True
        
    if all(metadata_files.values()):
        output = "true"
        evidence = constants.EVIDENCE_METADATA_EXISTS
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_METADATA_EXISTS
        
        missing_metadata = [key for key, value in metadata_files.items() if not value]
        missing_metadata_txt = ', '.join(missing_metadata)
        
        evidence += missing_metadata_txt
    
    
    check = ch.Check(constants.INDICATORS_DICT['descriptive_metadata'], 'RSFC-04-1', constants.PROCESS_METADATA_EXISTS, output, evidence)
    
    return check.convert()


def test_readme_exists(somef_data):
    if 'readme_url' in somef_data:
        output = "true"
        evidence = constants.EVIDENCE_DOCUMENTATION_README
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_DOCUMENTATION_README
        
    check = ch.Check(constants.INDICATORS_DICT['software_documentation'], 'RSFC-04-2', constants.PROCESS_README, output, evidence)
    
    return check.convert()


def test_title_description(somef_data):
    if 'full_title' in somef_data:
        title = True
    else:
        title = False
        
    if 'description' in somef_data:
        desc = True
    else:
        desc = False
        
    if title and desc:
        output = "true"
        evidence = constants.EVIDENCE_TITLE_AND_DESCRIPTION
    elif title and not desc:
        output = "false"
        evidence = constants.EVIDENCE_NO_DESCRIPTION
    elif desc and not title:
        output = "false"
        evidence = constants.EVIDENCE_NO_TITLE
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_TITLE_AND_DESCRIPTION
        
        
    check = ch.Check(constants.INDICATORS_DICT['descriptive_metadata'], 'RSFC-04-3', constants.PROCESS_TITLE_DESCRIPTION, output, evidence)
    
    return check.convert()


def test_descriptive_metadata(somef_data):
    
    metadata = {
        'description': None,
        'programming_languages': None,
        'date_created': None,
        'keywords': None
    }
    
    metadata = {key: key in somef_data for key in metadata}
        
        
    if all(metadata.values()):
        output = "true"
        evidence = constants.EVIDENCE_DESCRIPTIVE_METADATA
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_DESCRIPTIVE_METADATA
        
        missing_metadata = [key for key, value in metadata.items() if not value]
        missing_metadata_txt = ', '.join(missing_metadata)
        
        evidence += missing_metadata_txt
        
    check = ch.Check(constants.INDICATORS_DICT['descriptive_metadata'], 'RSFC-04-4', constants.PROCESS_DESCRIPTIVE_METADATA, output, evidence)
    
    return check.convert()
        
        

def test_codemeta_exists(codemeta_data):
    if codemeta_data != None:
        output = "true"
        evidence = constants.EVIDENCE_METADATA_CODEMETA
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_METADATA_CODEMETA
    
    check = ch.Check(constants.INDICATORS_DICT['descriptive_metadata'], 'RSFC-04-5', constants.PROCESS_CODEMETA, output, evidence)
    
    return check.convert()

################################################### FRSM_05 ###################################################

def test_repo_status(somef_data):
    if 'repository_status' in somef_data:
        output = "true"
        evidence = constants.EVIDENCE_REPO_STATUS
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_REPO_STATUS
        
        
    check = ch.Check(constants.INDICATORS_DICT['version_control_use'], 'RSFC-05-1', constants.PROCESS_REPO_STATUS, output, evidence)
    
    return check.convert()


def test_contact_support_documentation(somef_data):
    sources = {
        'contact': None,
        'support': None,
        'support_channels': None
    }
    
    sources = {key: key in somef_data for key in sources}
        
        
    if all(sources.values()):
        output = "true"
        evidence = constants.EVIDENCE_CONTACT_INFO
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_CONTACT_INFO
        
        missing_sources = [key for key, value in sources.items() if not value]
        missing_sources_txt = ', '.join(missing_sources)
        
        evidence += missing_sources_txt
        
    check = ch.Check(constants.INDICATORS_DICT['software_documentation'], 'RSFC-05-2', constants.PROCESS_CONTACT_SUPPORT_DOCUMENTATION, output, evidence)
    
    return check.convert()


def test_software_documentation(somef_data):
    rtd = False
    readme = False
    
    sources = ''
    
    if 'documentation' in somef_data:
        for item in somef_data['documentation']:
            if 'readthedocs' in item['result']['value']:
                rtd = True
                if item['source'] not in sources:
                    sources += f"\t\n- {item['source']}"
    if 'readme_url' in somef_data:
        readme = True
        for item in somef_data['readme_url']:
            if item['result']['value'] not in sources:
                sources += f"\t\n- {item['result']['value']}"
        
        
    if not readme and not rtd:
        output = "false"
        evidence = constants.EVIDENCE_NO_README_AND_READTHEDOCS
    else:
        evidence = constants.EVIDENCE_DOCUMENTATION + sources
        output = "true"
        
        
    check = ch.Check(constants.INDICATORS_DICT['software_documentation'], 'RSFC-05-3', constants.PROCESS_DOCUMENTATION, output, evidence)
    
    return check.convert()

################################################### FRSM_06 ###################################################

def test_authors(somef_data, codemeta_data, cff_data):
    
    if 'authors' in somef_data:
        evidence = constants.EVIDENCE_AUTHORS
        output = "true"
    elif codemeta_data != None and codemeta_data["author"] != None:
        output = "true"
        evidence = constants.EVIDENCE_AUTHORS
    elif cff_data != None and cff_data["authors"] != None:
        output = "true"
        evidence = constants.EVIDENCE_AUTHORS
    else:
        evidence = constants.EVIDENCE_NO_AUTHORS
        output = "false"

        
    check = ch.Check(constants.INDICATORS_DICT['descriptive_metadata'], 'RSFC-06-1', constants.PROCESS_AUTHORS, output, evidence)
    
    return check.convert()


def test_contributors(somef_data, codemeta_data):
    
    if 'contributors' in somef_data:
        output = "true"
        evidence = constants.EVIDENCE_CONTRIBUTORS
    elif codemeta_data != None and codemeta_data["contributor"] != None:
        output = "true"
        evidence = constants.EVIDENCE_CONTRIBUTORS
    else:
        evidence = constants.EVIDENCE_NO_CONTRIBUTORS
        output = "false"
        
    check = ch.Check(constants.INDICATORS_DICT['descriptive_metadata'], 'RSFC-06-2', constants.PROCESS_CONTRIBUTORS, output, evidence)
    
    return check.convert()


def test_authors_orcids(codemeta_data, cff_data):
    author_orcids_codemeta = False
    author_orcids_cff = None
    
    if codemeta_data != None:
        if codemeta_data["author"] != None:
            author_orcids_codemeta = rsfc_helpers.subtest_author_orcids(codemeta_data)
    
    if cff_data != None:
        if cff_data["authors"] != None:
            author_orcids_cff = rsfc_helpers.subtest_author_orcids(cff_data)
    
    if author_orcids_codemeta and author_orcids_cff:
        output = "true"
        evidence = constants.EVIDENCE_AUTHOR_ORCIDS_BOTH
    elif author_orcids_codemeta:
        output = "true"
        evidence = constants.EVIDENCE_AUTHOR_ORCIDS_CODEMETA
    elif author_orcids_cff:
        output = "true"
        evidence = constants.EVIDENCE_AUTHOR_ORCIDS_CFF
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_AUTHOR_ORCIDS
        
    check = ch.Check(constants.INDICATORS_DICT['descriptive_metadata'], 'RSFC-06-3', constants.PROCESS_AUTHOR_ORCIDS, output, evidence)
    
    return check.convert()


def test_author_roles(codemeta_data):
    
    if codemeta_data != None:
        if codemeta_data["author"] != None:
            author_roles = rsfc_helpers.subtest_author_roles(codemeta_data["author"])
            
            if all(value is not None for value in author_roles.values()):
                output = "true"
                evidence = constants.EVIDENCE_AUTHOR_ROLES
            else:
                output = "false"
                evidence = constants.EVIDENCE_NO_ALL_AUTHOR_ROLES
        else:
            output = "false"
            evidence = constants.EVIDENCE_NO_AUTHORS_IN_CODEMETA
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_CODEMETA_FOUND
        
    check = ch.Check(constants.INDICATORS_DICT['descriptive_metadata'], 'RSFC-06-4', constants.PROCESS_AUTHOR_ROLES, output, evidence)
    
    return check.convert()

################################################### FRSM_07 ###################################################

def test_identifier_in_readme_citation(somef_data, cff_data):
    readme = False
    citation = False
    
    if 'identifier' in somef_data:
        readme = True
        
    if cff_data != None:
        if cff_data["identifiers"] != None:
            citation = True
        
    if readme and not citation:
        output = "true"
        evidence = constants.EVIDENCE_IDENTIFIER_IN_README
    elif citation and not readme:
        output = "true"
        evidence = constants.EVIDENCE_IDENTIFIER_IN_CITATION
    elif citation and readme:
        output = "true"
        evidence = constants.EVIDENCE_IDENTIFIER_IN_README_AND_CITATION
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_IDENTIFIER_IN_README_OR_CITATION
        
        
    check = ch.Check(constants.INDICATORS_DICT['persistent_and_unique_identifier'], 'RSFC-07-1', constants.PROCESS_IDENTIFIER_IN_README_CITATION, output, evidence)
    
    return check.convert()


def test_identifier_resolves_to_software(somef_data, codemeta_data, cff_data, repo_url):
    
    output = "false"
    evidence = constants.EVIDENCE_NO_IDENTIFIER_FOUND
    identifier = None
    pause = False

    if 'identifier' in somef_data:
        for item in somef_data['identifier']:
            if item['source']:
                if 'README' in item['source']:
                    identifier = item['result']['value']
                    pause = True
                    break
                    
    if not pause and codemeta_data != None and codemeta_data['identifier']:
        identifier = codemeta_data['identifier']
        
    if not pause and cff_data != None and cff_data['identifiers'] != None:
        identifier = cff_data['identifiers'][0]['value']
        
    if identifier:
        doi_url = rsfc_helpers.normalize_identifier_url(identifier)
        try:
            resp = requests.get(doi_url, allow_redirects=True, timeout=10)
            html = resp.text
            
            if rsfc_helpers.landing_page_links_back(html, repo_url):
                output = "true"
                evidence = constants.EVIDENCE_DOI_LINKS_BACK_TO_REPO
            else:
                output = "false"
                evidence = constants.EVIDENCE_DOI_NO_LINK_BACK_TO_REPO
                
        except requests.RequestException:
            output = "false"
            evidence = constants.EVIDENCE_NO_RESOLVE_DOI_IDENTIFIER


    check = ch.Check(constants.INDICATORS_DICT['persistent_and_unique_identifier'], 'RSFC-07-2', constants.PROCESS_ID_RESOLVES_TO_SOFTWARE, output, evidence)
    
    return check.convert()

################################################### FRSM_08 ###################################################

def test_metadata_record_in_zenodo_or_software_heritage(somef_data): #CAMBIAR
    zenodo = False
    swh = False
    
    if 'identifier' in somef_data:
        for item in somef_data['identifier']:
            if item['result']['value'] and ('zenodo' in item['result']['value'] or 'softwareheritage' in item['result']['value']):
                    if 'zenodo' in item['result']['value']:
                        zenodo = True
                    elif 'softwareheritage' in item['result']['value']:
                        swh = True
                    else:
                        continue
            
    if zenodo and swh:
        output = "true"
        evidence = constants.EVIDENCE_ZENODO_DOI_AND_SOFTWARE_HERITAGE
    elif swh:
        output = "true"
        evidence = constants.EVIDENCE_SOFTWARE_HERITAGE_BADGE
    elif zenodo:
        output = "true"
        evidence = constants.EVIDENCE_ZENODO_DOI
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_ZENODO_DOI_OR_SOFTWARE_HERITAGE
        
        
    check = ch.Check(constants.INDICATORS_DICT['archived_in_software_heritage'], 'RSFC-08-1', constants.PROCESS_ZENODO_SOFTWARE_HERITAGE, output, evidence)
    
    return check.convert()

################################################### FRSM_09 ###################################################

def test_is_github_repository(repo_url):

    if 'github.com' in repo_url or 'gitlab.com' in repo_url:
        response = requests.head(repo_url, allow_redirects=True, timeout=5)
        if response.status_code == 200:
            output = "true"
            evidence = constants.EVIDENCE_IS_IN_GITHUB_OR_GITLAB
        elif response.status_code == 404:
            output = "false"
            evidence = constants.EVIDENCE_NO_RESOLVE_GITHUB_OR_GITLAB_URL
        else:
            output = "false"
            evidence = 'Connection error'
    else:
        output = "true"
        evidence = constants.EVIDENCE_NO_GITHUB_OR_GITLAB_URL
        
    
    check = ch.Check(constants.INDICATORS_DICT['version_control_use'], 'RSFC-09-1', constants.PROCESS_IS_GITHUB_OR_GITLAB_REPOSITORY, output, evidence)
    
    return check.convert()

################################################### FRSM_12 ###################################################

def test_reference_publication(somef_data, codemeta_data):
    
    referencePub = False
        
    if codemeta_data != None and codemeta_data["referencePublication"] != None:
        referencePub = True
    
    article_citation = False
    
    if 'citation' in somef_data:
        for item in somef_data['citation']:
            if 'format' in item['result'] and item['result']['format'] == 'bibtex':
                article_citation = True
                break
            
    
    if article_citation and referencePub:
        output = "true"
        evidence = constants.EVIDENCE_REFERENCE_PUBLICATION_AND_CITATION_TO_ARTICLE
    elif article_citation:
        output = "true"
        evidence = constants.EVIDENCE_CITATION_TO_ARTICLE
    elif referencePub:
        output = "true"
        evidence = constants.EVIDENCE_REFERENCE_PUBLICATION
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_REFERENCE_PUBLICATION_OR_CITATION_TO_ARTICLE
        
        
    check = ch.Check(constants.INDICATORS_DICT['software_has_citation'], 'RSFC-12-1', constants.PROCESS_REFERENCE_PUBLICATION, output, evidence)
    
    return check.convert()

################################################### FRSM_13 ###################################################

def test_dependencies_declared(somef_data):
    if 'requirements' not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_DEPENDENCIES
    else:
        output = "true"
        evidence = constants.EVIDENCE_DEPENDENCIES
        
        for item in somef_data['requirements']:
            if 'source' in item:
                if item['source'] not in evidence:
                    evidence += f'\n\t- {item["source"]}'

    check = ch.Check(constants.INDICATORS_DICT['requirements_specified'], 'RSFC-13-1', constants.PROCESS_REQUIREMENTS, output, evidence)
    
    return check.convert()


def test_installation_instructions(somef_data):
    if 'installation' in somef_data:
        output = "true"
        evidence = constants.EVIDENCE_INSTALLATION
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_INSTALLATION
        
    check = ch.Check(constants.INDICATORS_DICT['software_documentation'], 'RSFC-13-2', constants.PROCESS_INSTALLATION, output, evidence)
    
    return check.convert()


def test_dependencies_have_version(somef_data):
    if 'requirements' not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_DEPENDENCIES
    else:
        output = "true"
        evidence = constants.EVIDENCE_DEPENDENCIES_VERSION
        for item in somef_data['requirements']:
            if 'README' not in item['source'] and item['result']['version']:
                continue
            else:
                output = "false"
                evidence = constants.EVIDENCE_NO_DEPENDENCIES_VERSION
                break
    
    check = ch.Check(constants.INDICATORS_DICT['requirements_specified'], 'RSFC-13-3', constants.PROCESS_DEPENDENCIES_VERSION, output, evidence)
    
    return check.convert()


def test_dependencies_in_machine_readable_file(somef_data):
    if 'requirements' not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_DEPENDENCIES
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_DEPENDENCIES_MACHINE_READABLE_FILE
        
        for item in somef_data['requirements']:
            if item['source'] and 'README' not in item['source']:
                output = "true"
                evidence = constants.EVIDENCE_DEPENDENCIES_MACHINE_READABLE_FILE
                break
            
    check = ch.Check(constants.INDICATORS_DICT['requirements_specified'], 'RSFC-13-4', constants.PROCESS_DEPENDENCIES_MACHINE_READABLE_FILE, output, evidence)
    
    return check.convert()


################################################### FRSM_14 ###################################################

def test_presence_of_tests(gh):
    
    test_evidences = gh.tests

    if test_evidences:
        rx = re.compile(r'tests?', re.IGNORECASE)
        sources = ""

        for e in test_evidences:
            path = e["path"]
            if rx.search(path):
                sources += f"\t\n- {path}"

        if sources:
            output = "true"
            evidence = constants.EVIDENCE_TESTS + sources
        else:
            output = "false"
            evidence = constants.EVIDENCE_NO_TESTS
    else:
        output = "error"
        evidence = None
            
            
    check = ch.Check(constants.INDICATORS_DICT['software_tests'], 'RSFC-14-1', constants.PROCESS_TESTS, output, evidence)
    
    return check.convert()


def test_github_action_tests(somef_data):
    sources = ''
    
    if 'continuous_integration' not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_WORKFLOWS
    else:
        for item in somef_data['continuous_integration']:
            if item['result']['value'] and ('.github/workflows' in item['result']['value'] or '.gitlab-ci.yml' in item['result']['value']):
                if 'test' in item['result']['value'] or 'tests' in item['result']['value']:
                    sources += f'\t\n- {item["result"]["value"]}'
                    
    if sources:
        output = "true"
        evidence = constants.EVIDENCE_AUTOMATED_TESTS + sources
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_AUTOMATED_TESTS

    check = ch.Check(constants.INDICATORS_DICT['repository_workflows'], 'RSFC-14-2', constants.PROCESS_AUTOMATED_TESTS, output, evidence)
    
    return check.convert()

################################################### FRSM_15 ###################################################

def test_has_license(somef_data):
    if 'license' not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_LICENSE
    else:
        output = "true"
        evidence = constants.EVIDENCE_LICENSE
        for item in somef_data['license']:
            if 'source' in item:
                evidence += f'\n\t- {item["source"]}'
                
    check = ch.Check(constants.INDICATORS_DICT['software_has_license'], 'RSFC-15-1', constants.PROCESS_LICENSE, output, evidence)
    
    return check.convert()


def test_license_spdx_compliant(somef_data):
    output = "false"
    evidence = None
    if 'license' not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_LICENSE
    else:
        for item in somef_data['license']:
            if 'result' in item and 'spdx_id' in item['result']:
                if item['result']['spdx_id'] in constants.SPDX_LICENSE_WHITELIST:
                    output = "true"
                else:
                    output = "false"
                    evidence = constants.EVIDENCE_NO_SPDX_COMPLIANT
                    break
        
        if output == "true":
            evidence = constants.EVIDENCE_SPDX_COMPLIANT
        elif output == "false" and evidence == None:
            evidence = constants.EVIDENCE_LICENSE_NOT_CLEAR
            
    check = ch.Check(constants.INDICATORS_DICT['software_has_license'], 'RSFC-15-2', constants.PROCESS_LICENSE_SPDX_COMPLIANT, output, evidence)
    
    return check.convert()


def test_license_information_provided(somef_data):
    
    if 'license' not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_LICENSE
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_LICENSE_INFORMATION_PROVIDED
        for item in somef_data['license']:
            if 'source' in item:
                if 'README' in item['source']:
                    output = "true"
                    evidence = constants.EVIDENCE_LICENSE_INFORMATION_PROVIDED
                    
                
    check = ch.Check(constants.INDICATORS_DICT['software_has_license'], 'RSFC-15-3', constants.PROCESS_LICENSE_INFORMATION_PROVIDED, output, evidence)
    
    return check.convert()

################################################### FRSM_16 ###################################################

def test_license_info_in_metadata_files(somef_data, codemeta_data, cff_data):
    
    license_info = {
        'codemeta': False,
        'citation': False,
        'package': False
    }
    
    if 'license' in somef_data:
        for item in somef_data['license']:
            if 'source' in item:
                if 'pyproject.toml' in item['source'] or 'setup.py' in item['source'] or 'node.json' in item['source'] or 'pom.xml' in item['source'] or 'package.json' in item['source']:
                    license_info['package'] = True
                    break
                    
    if cff_data != None and cff_data["license"] != None:
        license_info["citation"] = True

    if codemeta_data != None and codemeta_data["license"] != None:
        license_info["codemeta"] = True
                
            
    if all(license_info.values()):
        output = "true"
        evidence = constants.EVIDENCE_LICENSE_INFO_IN_METADATA
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_LICENSE_INFO_IN_METADATA
        
        missing_license_info= [key for key, value in license_info.items() if not value]
        missing_license_info_txt = ', '.join(missing_license_info)
        
        evidence += missing_license_info_txt
        
        
    check = ch.Check(constants.INDICATORS_DICT['software_has_license'], 'RSFC-16-1', constants.PROCESS_LICENSE_INFO_IN_METADATA_FILES, output, evidence)
    
    return check.convert()

################################################### FRSM_17 ###################################################

def test_repo_enabled_and_commits(somef_data, gh):
    
    if 'repository_status' in somef_data and somef_data['repository_status'][0]['result']['value']:
        if '#active' in somef_data['repository_status'][0]['result']['value']:
            repo = True
        else:
            repo = False
    else:
        repo = False
        
    commits = gh.commits

    if repo:
        if commits:
            output = "true"
            evidence = constants.EVIDENCE_REPO_ENABLED_AND_HAS_COMMITS
        else:
            output = "false"
            evidence = constants.EVIDENCE_NO_COMMITS
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_REPO_STATUS
        
        
    check = ch.Check(constants.INDICATORS_DICT['version_control_use'], 'RSFC-17-1', constants.PROCESS_REPO_ENABLED_AND_COMMITS, output, evidence)
    
    return check.convert()


def test_commit_history(gh):

    commits = gh.commits
    
    if commits != []:
        output = "true"
        evidence = constants.EVIDENCE_COMMITS
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_COMMITS
        
    check = ch.Check(constants.INDICATORS_DICT['version_control_use'], 'RSFC-17-2', constants.PROCESS_COMMITS_HISTORY, output, evidence)
    
    return check.convert()

def test_commits_linked_issues(gh):
    
    commits = gh.commits
    issues = gh.issues

    if commits == [] or issues == []:
        output = "false"
        evidence = constants.EVIDENCE_NOT_ENOUGH_ISSUES_COMMITS_INFO
    else:
        linked = rsfc_helpers.cross_check_any_issue(issues, commits)
        
        if linked:
            output = "true"
            evidence = constants.EVIDENCE_COMMITS_LINKED_TO_ISSUES
        else:
            output = "false"
            evidence = constants.EVIDENCE_NO_COMMITS_LINKED_TO_ISSUES
            

    check = ch.Check(constants.INDICATORS_DICT['version_control_use'], 'RSFC-17-3', constants.PROCESS_COMMITS_LINKED_TO_ISSUES, output, evidence)
    
    return check.convert()


################################################### MISC ###################################################


def test_has_citation(somef_data):
    if 'citation' not in somef_data:
            output = "false"
            evidence = constants.EVIDENCE_NO_CITATION
    else:
        output = "true"
        evidence = constants.EVIDENCE_CITATION
        for item in somef_data['citation']:
            if 'source' in item:
                if item['source'] not in evidence:
                    evidence += f'\n\t- {item["source"]}'
        
    check = ch.Check(constants.INDICATORS_DICT['software_has_citation'], 'RSFC-18-1', constants.PROCESS_CITATION, output, evidence)
    
    return check.convert()


def test_repository_workflows(somef_data):

    if 'continuous_integration' not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_WORKFLOWS
    else:
        output = "true"
        evidence = constants.EVIDENCE_WORKFLOWS
    
        for item in somef_data['continuous_integration']:
            evidence += f'\n\t- {item["result"]["value"]}'

    check = ch.Check(constants.INDICATORS_DICT['repository_workflows'], 'RSFC-19-1', constants.PROCESS_WORKFLOWS, output, evidence)
    
    return check.convert()
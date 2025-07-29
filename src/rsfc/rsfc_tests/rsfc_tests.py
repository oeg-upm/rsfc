from rsfc.utils import constants
from rsfc.model import check as ch
import regex as re
import requests
import json
import urllib
from rsfc.utils import rsfc_helpers


################################################### FRSM_01 ###################################################

def test_id_presence_and_resolves(repo_data):
    if 'identifier' in repo_data:
        for item in repo_data['identifier']:
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
                        except requests.RequestException as e:
                            output = "false"
                            evidence = None
                    else:
                        output = "false"
                        evidence = constants.EVIDENCE_ID_NOT_URL
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_IDENTIFIER_FOUND
                        
    
    check = ch.Check(constants.INDICATORS_DICT['persistent_and_unique_identifier'], constants.PROCESS_IDENTIFIER, output, evidence)
    
    return check.convert()


def test_id_proper_schema(repo_data):
    if 'identifier' in repo_data:
        compiled_patterns = []
        for pattern in constants.ID_SCHEMA_REGEX_LIST:
            compiled = re.compile(pattern)
            compiled_patterns.append(compiled)
            
        output = "true"
        evidence = constants.EVIDENCE_ID_PROPER_SCHEMA
            
        for item in repo_data['identifier']:
            if not any(pattern.match(item['result']['value']) for pattern in compiled_patterns):
                output = "false"
                evidence = constants.EVIDENCE_NO_ID_PROPER_SCHEMA
                break
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_IDENTIFIER_FOUND
        
    
    check = ch.Check(constants.INDICATORS_DICT['persistent_and_unique_identifier'], constants.PROCESS_ID_PROPER_SCHEMA, output, evidence)
    
    return check.convert()


def test_id_associated_with_software(repo_data, repo_url, repo_type, repo_branch):
    
    id_locations = {
        'codemeta_id': False,
        'referencePublication': False,
        'citation': False,
        'readme': False
    }
    
    base_url = rsfc_helpers.get_repo_api_url(repo_url, repo_type)
    codemeta_content = None

    if repo_type == "GITHUB":
        headers = {'Accept': 'application/vnd.github.v3+json'}
        url = base_url + "/contents/codemeta.json"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            content_json = response.json()
            codemeta_content = rsfc_helpers.decode_github_content(content_json)

    elif repo_type == "GITLAB":
        file_path = urllib.parse.quote("codemeta.json", safe="")
        url = f"{base_url}/repository/files/{file_path}/raw?ref={repo_branch}"
        response = requests.get(url)

        if response.status_code == 200:
            codemeta_content = response.text

    else:
        raise ValueError("Unsupported repository type")

    if codemeta_content:
        codemeta_json = json.loads(codemeta_content)

        if 'identifier' in codemeta_json:
            id_locations['codemeta_id'] = True
            
        if 'referencePublication' in codemeta_json:
            for item in codemeta_json['referencePublication']:
                if item['identifier']:
                    id_locations['referencePub'] = True
                    break
    

    if 'citation' in repo_data:
        for item in repo_data['citation']:
            if item['source']:
                if 'CITATION.cff' in item['source']:
                    if 'identifiers:' in item['result']['value']:
                        id_locations['citation'] = True
        
    
    if 'identifier' in repo_data:
        id_locations['readme'] = True
        
        
    if all(id_locations.values()):
        output = "true"
        evidence = constants.EVIDENCE_ID_ASSOCIATED_WITH_SOFTWARE
    elif any(id_locations.values()):
        output = "improvable"
        evidence = constants.EVIDENCE_SOME_ID_ASSOCIATED_WITH_SOFTWARE
        
        missing_id_locations = [key for key, value in id_locations.items() if not value]
        missing_id_locations_txt = ', '.join(missing_id_locations)
        
        evidence += missing_id_locations_txt
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_ID_ASSOCIATED_WITH_SOFTWARE
    
        
        
    check = ch.Check(constants.INDICATORS_DICT['persistent_and_unique_identifier'], constants.PROCESS_ID_ASSOCIATED_WITH_SOFTWARE, output, evidence)
    
    return check.convert()



################################################### FRSM_03 ###################################################

def test_has_releases(repo_data):
    if 'releases' not in repo_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_RELEASES
    else:
        output = "true"
        evidence = constants.EVIDENCE_RELEASES
        for item in repo_data['releases']:
            if 'type' in item['result']:
                if item['result']['type'] == 'Release':
                    if 'name' in item['result']:
                        # evidence += f'\n\t- {item['result']['name']}'
                        evidence += f'\n\t- {item["result"]["name"]}'
                    elif 'tag' in item['result']:
                        # evidence += f'\n\t- {item['result']['tag']}'
                        evidence += f'\n\t- {item["result"]["tag"]}'
                    else:
                        # evidence += f'\n\t- {item['result']['url']}'
                        evidence += f'\n\t- {item["result"]["url"]}'
                        
    check = ch.Check(constants.INDICATORS_DICT['has_releases'], constants.PROCESS_RELEASES, output, evidence)

    return check.convert()
    
    
def test_release_id_and_version(repo_data):
    if 'releases' not in repo_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_RELEASES
    else:
        results = repo_data['releases']
        for item in results:
            if item['result']['url'] and item['result']['tag']:
                output = "true"
                evidence = constants.EVIDENCE_RELEASE_ID_AND_VERSION
            else:
                output = "false"
                evidence = constants.EVIDENCE_NO_RELEASE_ID_AND_VERSION
                break
                
    check = ch.Check(constants.INDICATORS_DICT['has_releases'], constants.PROCESS_RELEASE_ID_VERSION, output, evidence)
    
    return check.convert()


def test_semantic_versioning_standard(repo_data):
    
    if 'releases' not in repo_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_RELEASES
    else:
        compiled_patterns = []
        for pattern in constants.VERSIONING_REGEX_LIST:
            compiled = re.compile(pattern)
            compiled_patterns.append(compiled)
            
        results = repo_data['releases']
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
                
    check = ch.Check(constants.INDICATORS_DICT['semantic_versioning'], constants.PROCESS_SEMANTIC_VERSIONING, output, evidence)
    
    return check.convert()
        
    
def test_version_scheme(repo_data):
    if 'releases' not in repo_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_RELEASES
    else:
        scheme = ''
        results = repo_data['releases']
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
        
    check = ch.Check(constants.INDICATORS_DICT['semantic_versioning'], constants.PROCESS_VERSION_SCHEME, output, evidence)
    
    return check.convert()



def test_latest_release_consistency(repo_data):
    latest_release = None
    version = None
    
    if 'releases' in repo_data:
        latest_release = rsfc_helpers.get_latest_release(repo_data)
        
    if 'version' in repo_data:
        version_data = repo_data['version'][0]['result']
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
        
        
    check = ch.Check(constants.INDICATORS_DICT['has_releases'], constants.PROCESS_RELEASE_CONSISTENCY, output, evidence)
    
    return check.convert()

################################################### FRSM_04 ###################################################

def test_metadata_exists(repo_data, repo_url, repo_type, repo_branch):
    
    metadata_files = {
        'citation': False,
        'codemeta': False,
        'package_file': False
    }
    
    if 'citation' in repo_data:
        metadata_files['citation'] = True
        
    if 'has_package_file' in repo_data:
        metadata_files['package_file'] = True
        
    base_url = rsfc_helpers.get_repo_api_url(repo_url, repo_type)
    if repo_type == "GITHUB":
        headers = {'Accept': 'application/vnd.github.v3+json'}
        url = base_url + "/contents/codemeta.json"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            metadata_files['codemeta'] = True

    elif repo_type == "GITLAB":
        file_path = urllib.parse.quote("codemeta.json", safe="")
        url = f"{base_url}/repository/files/{file_path}?ref={repo_branch}"
        response = requests.head(url)

        if response.status_code == 200:
            metadata_files['codemeta'] = True
        
    if all(metadata_files.values()):
        output = "true"
        evidence = constants.EVIDENCE_METADATA_EXISTS
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_METADATA_EXISTS
        
        missing_metadata = [key for key, value in metadata_files.items() if not value]
        missing_metadata_txt = ', '.join(missing_metadata)
        
        evidence += missing_metadata_txt
    
    
    check = ch.Check(constants.INDICATORS_DICT['descriptive_metadata'], constants.PROCESS_METADATA_EXISTS, output, evidence)
    
    return check.convert()


def test_readme_exists(repo_data):
    if 'readme_url' in repo_data:
        output = "true"
        evidence = constants.EVIDENCE_DOCUMENTATION_README
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_DOCUMENTATION_README
        
    check = ch.Check(constants.INDICATORS_DICT['software_documentation'], constants.PROCESS_README, output, evidence)
    
    return check.convert()


def test_title_description(repo_data):
    if 'full_title' in repo_data:
        title = True
    else:
        title = False
        
    if 'description' in repo_data:
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
        
        
    check = ch.Check(constants.INDICATORS_DICT['descriptive_metadata'], constants.PROCESS_TITLE_DESCRIPTION, output, evidence)
    
    return check.convert()


def test_descriptive_metadata(repo_data):
    
    metadata = {
        'description': None,
        'programming_languages': None,
        'date_created': None,
        'keywords': None
    }
    
    metadata = {key: key in repo_data for key in metadata}
        
        
    if all(metadata.values()):
        output = "true"
        evidence = constants.EVIDENCE_DESCRIPTIVE_METADATA
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_DESCRIPTIVE_METADATA
        
        missing_metadata = [key for key, value in metadata.items() if not value]
        missing_metadata_txt = ', '.join(missing_metadata)
        
        evidence += missing_metadata_txt
        
    check = ch.Check(constants.INDICATORS_DICT['descriptive_metadata'], constants.PROCESS_DESCRIPTIVE_METADATA, output, evidence)
    
    return check.convert()
        
        

def test_codemeta_exists(repo_url, repo_type, repo_branch):
    base_url = rsfc_helpers.get_repo_api_url(repo_url, repo_type)
    if repo_type == "GITHUB":
        headers = {'Accept': 'application/vnd.github.v3+json'}
        url = base_url + "/contents/codemeta.json"
        response = requests.get(url, headers=headers)

    elif repo_type == "GITLAB":
        file_path = urllib.parse.quote("codemeta.json", safe="")
        url = f"{base_url}/repository/files/{file_path}?ref={repo_branch}"
        response = requests.head(url)

    else:
        raise ValueError("Unsupported repository type")

    if response.status_code == 200:
        output = "true"
        evidence = constants.EVIDENCE_METADATA_CODEMETA
    elif response.status_code == 404:
        output = "false"
        evidence = constants.EVIDENCE_NO_METADATA_CODEMETA
    else:
        raise ConnectionError(f"Error accessing the repository: {response.status_code}")
    
    check = ch.Check(constants.INDICATORS_DICT['descriptive_metadata'], constants.PROCESS_CODEMETA, output, evidence)
    
    return check.convert()

################################################### FRSM_05 ###################################################

def test_repo_status(repo_data):
    if 'repository_status' in repo_data:
        output = "true"
        evidence = constants.EVIDENCE_REPO_STATUS
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_REPO_STATUS
        
        
    check = ch.Check(constants.INDICATORS_DICT['version_control_use'], constants.PROCESS_REPO_STATUS, output, evidence)
    
    return check.convert()


def test_contact_support_documentation(repo_data):
    sources = {
        'contact': None,
        'support': None,
        'support_channels': None
    }
    
    sources = {key: key in repo_data for key in sources}
        
        
    if all(sources.values()):
        output = "true"
        evidence = constants.EVIDENCE_CONTACT_INFO
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_CONTACT_INFO
        
        missing_sources = [key for key, value in sources.items() if not value]
        missing_sources_txt = ', '.join(missing_sources)
        
        evidence += missing_sources_txt
        
    check = ch.Check(constants.INDICATORS_DICT['software_documentation'], constants.PROCESS_CONTACT_SUPPORT_DOCUMENTATION, output, evidence)
    
    return check.convert()


def test_software_documentation(repo_data):
    rtd = False
    readme = False
    
    sources = ''
    
    if 'documentation' in repo_data:
        for item in repo_data['documentation']:
            if 'readthedocs' in item['result']['value']:
                rtd = True
                if item['source'] not in sources:
                    sources += f"\t\n- {item['source']}"
    if 'readme_url' in repo_data:
        readme = True
        if item['result']['value'] not in sources:
            sources += f"\t\n- {item['result']['value']}"
        
        
    if not readme and not rtd:
        output = "false"
        evidence = constants.EVIDENCE_NO_README_AND_READTHEDOCS
    else:
        evidence = constants.EVIDENCE_DOCUMENTATION + sources
        output = "true"
        
        
    check = ch.Check(constants.INDICATORS_DICT['software_documentation'], constants.PROCESS_DOCUMENTATION, output, evidence)
    
    return check.convert()

################################################### FRSM_06 ###################################################

#Tiene que haber otra forma de averiguar los contributors
def test_authors_contribs(repo_data):
    authors = False
    contribs = False
    
    if 'authors' in repo_data:
        authors = True
    else:
        evidence = constants.EVIDENCE_NO_AUTHORS
        output = "false"
        
    if 'contributors' in repo_data:
        contribs = True
    else:
        evidence = constants.EVIDENCE_NO_CONTRIBUTORS
        output = "false"
        
    if authors and contribs:
        evidence = constants.EVIDENCE_AUTHORS_AND_CONTRIBUTORS
        output = "true"
        
    check = ch.Check(constants.INDICATORS_DICT['descriptive_metadata'], constants.PROCESS_AUTHORS_AND_CONTRIBS, output, evidence)
    
    return check.convert()


def test_authors_orcids(repo_data):
    
    if 'citation' in repo_data:
        if repo_data['citation'][0]['result']['author']:
            authors = repo_data['citation'][0]['result']['author']
            output = "true"
            evidence = constants.EVIDENCE_AUTHOR_ORCIDS
            for author in authors:
                if 'url' not in author:
                    output = "false"
                    evidence = constants.EVIDENCE_NO_AUTHOR_ORCIDS
                    break
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_CITATION
        
    check = ch.Check(constants.INDICATORS_DICT['descriptive_metadata'], constants.PROCESS_AUTHOR_ORCIDS, output, evidence)
    
    return check.convert()


def test_author_roles(repo_url, repo_type, repo_branch):
    base_url = rsfc_helpers.get_repo_api_url(repo_url, repo_type)
    if repo_type == "GITHUB":
        headers = {'Accept': 'application/vnd.github.v3+json'}
        url = base_url + "/contents/codemeta.json"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            content_json = response.json()
            codemeta_content = rsfc_helpers.decode_github_content(content_json)
            try:
                codemeta = json.loads(codemeta_content)
                output, evidence = rsfc_helpers.subtest_author_and_role(codemeta)
            except json.JSONDecodeError:
                raise ValueError("Not a valid codemeta.json file")
        elif response.status_code == 404:
            output = "false"
            evidence = constants.EVIDENCE_NO_METADATA_CODEMETA
        else:
            output = "false"
            evidence = None

    elif repo_type == "GITLAB":
        file_path = urllib.parse.quote("codemeta.json", safe="")
        url = f"{base_url}/repository/files/{file_path}/raw?ref={repo_branch}"
        response = requests.get(url)

        if response.status_code == 200:
            codemeta_content = response.text
            try:
                codemeta = json.loads(codemeta_content)
                output, evidence = rsfc_helpers.subtest_author_and_role(codemeta)
            except json.JSONDecodeError:
                raise ValueError("El archivo codemeta.json no es un JSON válido.")
        elif response.status_code == 404:
            output = "false"
            evidence = constants.EVIDENCE_NO_METADATA_CODEMETA
        else:
            output = "false"
            evidence = None

    else:
        raise ValueError("Unsupported repository type")
        
        
    check = ch.Check(constants.INDICATORS_DICT['descriptive_metadata'], constants.PROCESS_AUTHOR_ROLES, output, evidence)
    
    return check.convert()

################################################### FRSM_07 ###################################################

def test_identifier_in_readme_citation(repo_data):
    readme = False
    citation = False
    
    if 'identifier' in repo_data:
        readme = True
        
    if 'citation' in repo_data:
        for item in repo_data['citation']:
            if item['source']:
                if 'CITATION.cff' in item['source']:
                    if 'identifiers:' in item['result']['value']:
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
        
        
    check = ch.Check(constants.INDICATORS_DICT['persistent_and_unique_identifier'], constants.PROCESS_IDENTIFIER_IN_README_CITATION, output, evidence)
    
    return check.convert()



def test_identifier_resolves_to_software(repo_data):
    
    output = "false"
    
    if 'identifier' in repo_data:
        for item in repo_data['identifier']:
            if item['source']:
                if 'README' in item['source']:
                    id = item['result']['value']
                    
                    response = requests.head(id, allow_redirects=True, timeout=5)
                    if response.status_code == 200:
                        output = "true"
                        evidence = constants.EVIDENCE_ID_RESOLVES
                    else:
                        evidence = constants.EVIDENCE_NO_RESOLVE_DOI_IDENTIFIER
                        break
                else:
                    evidence = constants.EVIDENCE_NO_DOCUMENTATION_README
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_IDENTIFIER_FOUND


    check = ch.Check(constants.INDICATORS_DICT['persistent_and_unique_identifier'], constants.PROCESS_ID_RESOLVES_TO_SOFTWARE, output, evidence)
    
    return check.convert()

################################################### FRSM_08 ###################################################

def test_metadata_record_in_zenodo_or_software_heritage(repo_data, repo_url, repo_type, repo_branch):
    zenodo = False
    swh = False
    
    if 'identifier' in repo_data:
        for item in repo_data['identifier']:
            if item['result']['value'] and 'zenodo' in item['result']['value']:
                    zenodo = True
    
    
    base_url = rsfc_helpers.get_repo_api_url(repo_url, repo_type)
    readme = None

    if repo_type == "GITHUB":
        url = base_url + "/readme"
        headers = {'Accept': 'application/vnd.github.v3.raw'}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            readme = response.text

    elif repo_type == "GITLAB":
        for filename in ["README.md", "README.rst", "README.txt", "README"]:
            file_path = urllib.parse.quote(filename, safe="")
            url = f"{base_url}/repository/files/{file_path}/raw?ref={repo_branch}"
            response = requests.get(url)
            if response.status_code == 200:
                readme = response.text
                break
    else:
        raise ValueError("Unsupported repository type")

    if readme:
        pattern = constants.REGEX_SOFTWARE_HERITAGE_BADGE
        match = re.search(pattern, readme)
        if match:
            swh = True
            
    if zenodo and not swh:
        output = "true"
        evidence = constants.EVIDENCE_ZENODO_DOI
    elif swh and not zenodo:
        output = "true"
        evidence = constants.EVIDENCE_SOFTWARE_HERITAGE_BADGE
    elif zenodo and swh:
        output = "true"
        evidence = constants.EVIDENCE_ZENODO_DOI_AND_SOFTWARE_HERITAGE
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_ZENODO_DOI_OR_SOFTWARE_HERITAGE
        
        
    check = ch.Check(constants.INDICATORS_DICT['archived_in_software_heritage'], constants.PROCESS_ZENODO_SOFTWARE_HERITAGE, output, evidence)
    
    return check.convert()

################################################### FRSM_09 ###################################################

def test_is_github_repository(repo_url):

    if 'github.com' in repo_url or 'gitlab.com':
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
        
    
    check = ch.Check(constants.INDICATORS_DICT['version_control_use'], constants.PROCESS_IS_GITHUB_OR_GITLAB_REPOSITORY, output, evidence)
    
    return check.convert()

################################################### FRSM_12 ###################################################

def test_reference_publication(repo_data, repo_url, repo_type, repo_branch):
    
    base_url = rsfc_helpers.get_repo_api_url(repo_url, repo_type)
    codemeta_content = None

    if repo_type == "GITHUB":
        headers = {'Accept': 'application/vnd.github.v3+json'}
        url = base_url + "/contents/codemeta.json"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            content_json = response.json()
            codemeta_content = rsfc_helpers.decode_github_content(content_json)

    elif repo_type == "GITLAB":
        file_path = urllib.parse.quote("codemeta.json", safe="")
        url = f"{base_url}/repository/files/{file_path}/raw?ref={repo_branch}"
        response = requests.get(url)

        if response.status_code == 200:
            codemeta_content = response.text

    else:
        raise ValueError("Unsupported repository type")

    if codemeta_content:
        try:
            codemeta = json.loads(codemeta_content)
            if 'referencePublication' in codemeta and codemeta['referencePublication']:
                referencePub = True
            else:
                referencePub = False
        except json.JSONDecodeError:
            referencePub = False
    elif response.status_code == 404:
        referencePub = False
    else:
        referencePub = False
        
    
    article_citation = False
    
    if 'citation' in repo_data:
        for item in repo_data['citation']:
            if 'format' in item['result'] and item['result']['format'] == 'bibtex':
                article_citation = True
                break
            
    
    if referencePub and not article_citation:
        output = "true"
        evidence = constants.EVIDENCE_REFERENCE_PUBLICATION
    elif article_citation and not referencePub:
        output = "true"
        evidence = constants.EVIDENCE_CITATION_TO_ARTICLE
    elif article_citation and referencePub:
        output = "true"
        evidence = constants.EVIDENCE_REFERENCE_PUBLICATION_AND_CITATION_TO_ARTICLE
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_REFERENCE_PUBLICATION_OR_CITATION_TO_ARTICLE
        
        
    check = ch.Check(constants.INDICATORS_DICT['software_has_citation'], constants.PROCESS_REFERENCE_PUBLICATION, output, evidence)
    
    return check.convert()

################################################### FRSM_13 ###################################################

def test_dependencies_declared(repo_data):
    if 'requirements' not in repo_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_DEPENDENCIES
    else:
        output = "true"
        evidence = constants.EVIDENCE_DEPENDENCIES
        
        for item in repo_data['requirements']:
            if 'source' in item:
                if item['source'] not in evidence:
                    # evidence += f'\n\t- {item['source']}'
                    evidence += f'\n\t- {item["source"]}'

    check = ch.Check(constants.INDICATORS_DICT['requirements_specified'], constants.PROCESS_REQUIREMENTS, output, evidence)
    
    return check.convert()


def test_installation_instructions(repo_data):
    if 'installation' in repo_data:
        output = "true"
        evidence = constants.EVIDENCE_INSTALLATION
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_INSTALLATION
        
    check = ch.Check(constants.INDICATORS_DICT['software_documentation'], constants.PROCESS_INSTALLATION, output, evidence)
    
    return check.convert()


def test_dependencies_have_version(repo_data):
    if 'requirements' not in repo_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_DEPENDENCIES
    else:
        output = "true"
        evidence = constants.EVIDENCE_DEPENDENCIES_VERSION
        for item in repo_data['requirements']:
            if 'README' not in item['source'] and item['result']['version']:
                continue
            else:
                output = "false"
                evidence = constants.EVIDENCE_NO_DEPENDENCIES_VERSION
                break
    
    check = ch.Check(constants.INDICATORS_DICT['requirements_specified'], constants.PROCESS_DEPENDENCIES_VERSION, output, evidence)
    
    return check.convert()


def test_dependencies_in_machine_readable_file(repo_data):
    if 'requirements' not in repo_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_DEPENDENCIES
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_DEPENDENCIES_MACHINE_READABLE_FILE
        
        for item in repo_data['requirements']:
            if item['source'] and 'README' not in item['source']:
                output = "true"
                evidence = constants.EVIDENCE_DEPENDENCIES_MACHINE_READABLE_FILE
                break
            
    check = ch.Check(constants.INDICATORS_DICT['requirements_specified'], constants.PROCESS_DEPENDENCIES_MACHINE_READABLE_FILE, output, evidence)
    
    return check.convert()


################################################### FRSM_14 ###################################################

def test_presence_of_tests(repo_url, repo_type, repo_branch):
    base_url = rsfc_helpers.get_repo_api_url(repo_url, repo_type)
    entries = []

    if repo_type == "GITHUB":
        tree_url = f"{base_url}/git/trees/HEAD?recursive=1"
        resp = requests.get(tree_url, headers={'Accept': 'application/vnd.github.v3+json'})
        if resp.status_code == 200:
            entries = resp.json().get("tree", [])

    elif repo_type == "GITLAB":
        tree_url = f"{base_url}/repository/tree?recursive=true&ref={repo_branch}&per_page=100"
        resp = requests.get(tree_url)
        if resp.status_code == 200:
            entries = [{"path": item["path"]} for item in resp.json()]

    else:
        raise ValueError("Unsupported repository type")

    if entries:
        rx = re.compile(r'tests?', re.IGNORECASE)
        sources = ""

        for e in entries:
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
            
            
    check = ch.Check(constants.INDICATORS_DICT['software_tests'], constants.PROCESS_TESTS, output, evidence)
    
    return check.convert()


def test_github_action_tests(repo_data):
    sources = ''
    
    if 'continuous_integration' not in repo_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_WORKFLOWS
    else:
        for item in repo_data['continuous_integration']:
            if item['result']['value'] and ('.github/workflows' in item['result']['value'] or '.gitlab-ci.yml' in item['result']['value']):
                if 'test' in item['result']['value'] or 'tests' in item['result']['value']:
                    # sources += f'\t\n- {item['result']['value']}'
                    sources += f'\t\n- {item["result"]["value"]}'
                    
    if sources:
        output = "true"
        evidence = constants.EVIDENCE_AUTOMATED_TESTS + sources
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_AUTOMATED_TESTS

    check = ch.Check(constants.INDICATORS_DICT['repository_workflows'], constants.PROCESS_AUTOMATED_TESTS, output, evidence)
    
    return check.convert()


def test_repository_workflows(repo_data):

    if 'continuous_integration' not in repo_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_WORKFLOWS
    else:
        output = "true"
        evidence = constants.EVIDENCE_WORKFLOWS
    
        for item in repo_data['continuous_integration']:
            # evidence += f'\n\t- {item['result']['value']}'
            evidence += f'\n\t- {item["result"]["value"]}'

    check = ch.Check(constants.INDICATORS_DICT['repository_workflows'], constants.PROCESS_WORKFLOWS, output, evidence)
    
    return check.convert()

################################################### FRSM_15 ###################################################

def test_has_license(repo_data):
    if 'license' not in repo_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_LICENSE
    else:
        output = "true"
        evidence = constants.EVIDENCE_LICENSE
        for item in repo_data['license']:
            if 'source' in item:
                # evidence += f'\n\t- {item['source']}'
                evidence += f'\n\t- {item["source"]}'
    check = ch.Check(constants.INDICATORS_DICT['software_has_license'], constants.PROCESS_LICENSE, output, evidence)
    
    return check.convert()



def test_license_spdx_compliant(repo_data):
    output = "false"
    evidence = None
    if 'license' not in repo_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_LICENSE
    else:
        for item in repo_data['license']:
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
            
    check = ch.Check(constants.INDICATORS_DICT['software_has_license'], constants.PROCESS_LICENSE_SPDX_COMPLIANT, output, evidence)
    
    return check.convert()

################################################### FRSM_16 ###################################################

def test_license_info_in_metadata_files(repo_data, repo_url, repo_type, repo_branch):
    
    license_info = {
        'codemeta': False,
        'citation': False,
        'package': False
    }
    
    if 'license' in repo_data:
        for item in repo_data['license']:
            if 'source' in item:
                if 'pyproject.toml' in item['source'] or 'setup.py' in item['source'] or 'node.json' in item['source'] or 'pom.xml' in item['source'] or 'package.json' in item['source']:
                    license_info['package'] = True
                    break
                    
                    
    if 'citation' in repo_data:
        if repo_data['citation'][0]['result']['value']:
            if 'license:' in repo_data['citation'][0]['result']['value']:
                license_info['citation'] = True
                
                
    base_url = rsfc_helpers.get_repo_api_url(repo_url, repo_type)
    if repo_type == "GITHUB":
        url = base_url + '/contents/codemeta.json'
        res = requests.get(url)

        if res.status_code == 200:
            content_json = res.json()
            decoded_content = rsfc_helpers.decode_github_content(content_json)
            codemeta_data = json.loads(decoded_content)

            if 'license' in codemeta_data:
                license_info['codemeta'] = True

    elif repo_type == "GITLAB":
        file_path = urllib.parse.quote('codemeta.json', safe='')
        url = f"{base_url}/repository/files/{file_path}/raw?ref={repo_branch}"
        res = requests.get(url)

        if res.status_code == 200:
            decoded_content = res.text
            codemeta_data = json.loads(decoded_content)

            if 'license' in codemeta_data:
                license_info['codemeta'] = True
                
            
    if all(license_info.values()):
        output = "true"
        evidence = constants.EVIDENCE_LICENSE_INFO_IN_METADATA
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_LICENSE_INFO_IN_METADATA
        
        missing_license_info= [key for key, value in license_info.items() if not value]
        missing_license_info_txt = ', '.join(missing_license_info)
        
        evidence += missing_license_info_txt
        
        
    check = ch.Check(constants.INDICATORS_DICT['software_has_license'], constants.PROCESS_LICENSE_INFO_IN_METADATA_FILES, output, evidence)
    
    return check.convert()

################################################### FRSM_17 ###################################################

def test_repo_enabled_and_commits(repo_data, repo_url, repo_type, repo_branch):
    
    if 'repository_status' in repo_data and repo_data['repository_status'][0]['result']['value']:
        if '#active' in repo_data['repository_status'][0]['result']['value']:
            repo = True
        else:
            repo = False
    else:
        repo = False
        
    base_url = rsfc_helpers.get_repo_api_url(repo_url, repo_type)
    if repo_type == "GITHUB":
        commit_url = base_url + "/commits"
        headers = {'Accept': 'application/vnd.github.v3.raw'}
        response = requests.get(commit_url, headers=headers)

    elif repo_type == "GITLAB":
        commit_url = f"{base_url}/repository/commits?ref_name={repo_branch}"
        response = requests.get(commit_url)

    else:
        raise ValueError("Unsupported repository type")
    
    
    if response.status_code == 200:
        json_data = response.json()
        if isinstance(json_data, list) and len(json_data) > 0:
            commits = True
        else:
            commits = False
    else:
        raise ConnectionError(f"Error accessing the repository: {response.status_code}")
    
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
        
        
    check = ch.Check(constants.INDICATORS_DICT['version_control_use'], constants.PROCESS_REPO_ENABLED_AND_COMMITS, output, evidence)
    
    return check.convert()
            


def test_has_tickets(repo_data):
    output = "false"
    evidence = constants.EVIDENCE_NO_TICKETS
    
    if 'issue_tracker' in repo_data:
        for item in repo_data['issue_tracker']:
            if item['technique'] == 'GitHub_API':
                output = "true"
                evidence = constants.EVIDENCE_TICKETS
                break
            
    check = ch.Check(constants.INDICATORS_DICT['version_control_use'], constants.PROCESS_TICKETS, output, evidence)
    
    return check.convert()


################################################### MISC ###################################################


def test_has_citation(repo_data):
    if 'citation' not in repo_data:
            output = "false"
            evidence = constants.EVIDENCE_NO_CITATION
    else:
        output = "true"
        evidence = constants.EVIDENCE_CITATION
        for item in repo_data['citation']:
            if 'source' in item:
                if item['source'] not in evidence:
                    # evidence += f'\n\t- {item['source']}'
                    evidence += f'\n\t- {item["source"]}'
        
    check = ch.Check(constants.INDICATORS_DICT['software_has_citation'], constants.PROCESS_CITATION, output, evidence)
    
    return check.convert()
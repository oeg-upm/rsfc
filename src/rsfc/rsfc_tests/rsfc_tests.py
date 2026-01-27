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
                                evidence = constants.EVIDENCE_ID_RESOLVES.format(id=id)
                                suggest = "No suggestions"
                            else:
                                output = "false"
                                evidence = constants.EVIDENCE_NO_ID_RESOLVE.format(id=id)
                                suggest = constants.SUGGEST_IDENTIFIER_NO_RESOLVE
                        except requests.RequestException:
                            output = "error"
                            evidence = "Something went wrong when trying to resolve the identifier"
                            suggest = None
                    else:
                        output = "false"
                        evidence = constants.EVIDENCE_ID_NOT_URL.format(id=id)
                        suggest = constants.SUGGEST_IDENTIFIER_NOT_HTTP
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_IDENTIFIER_FOUND
        suggest = constants.SUGGEST_NO_IDENTIFIER
                        
    
    check = ch.Check(constants.INDICATORS_DICT['persistent_and_unique_identifier'], 'RSFC-01-1', "There is an identifier and resolves", constants.PROCESS_IDENTIFIER, output, evidence, suggest)
    
    return check.convert()


def test_id_common_schema(somef_data):
    if 'identifier' in somef_data:
        compiled_patterns = []
        for pattern in constants.ID_SCHEMA_REGEX_LIST:
            compiled = re.compile(pattern, re.IGNORECASE)
            compiled_patterns.append(compiled)
            
        output = "true"
        evidence = constants.EVIDENCE_ID_COMMON_SCHEMA
        suggest = "No suggestions"
            
        for item in somef_data['identifier']:
            if item['source']:
                if 'README' in item['source']:
                    if not any(pattern.match(item['result']['value']) for pattern in compiled_patterns):
                        output = "false"
                        evidence = constants.EVIDENCE_NO_ID_COMMON_SCHEMA
                        suggest = constants.SUGGEST_IDENTIFIER_SCHEME
                        break
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_IDENTIFIER_FOUND_README
        suggest = constants.SUGGEST_NO_IDENTIFIER
        
    
    check = ch.Check(constants.INDICATORS_DICT['persistent_and_unique_identifier'], 'RSFC-01-3', "Software identifier follows a proper schema", constants.PROCESS_ID_PROPER_SCHEMA, output, evidence, suggest)
    
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
            if 'source' in item:
                if 'README.md' in item['source']:
                    id_locations['readme'] = True
        
        
    if any(id_locations.values()):
        output = "true"
        evidence = constants.EVIDENCE_SOME_ID_ASSOCIATED_WITH_SOFTWARE
        suggest = "No suggestions"
        
        existing_id_locations = [key for key, value in id_locations.items() if not value]
        existing_id_locations_txt = ', '.join(existing_id_locations)
        
        evidence += existing_id_locations_txt
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_ID_ASSOCIATED_WITH_SOFTWARE
        suggest = constants.SUGGEST_IDENTIFIER_ASSOCIATED
    

    check = ch.Check(constants.INDICATORS_DICT['persistent_and_unique_identifier'], 'RSFC-01-2', "There is an identifier associated with the software", constants.PROCESS_ID_ASSOCIATED_WITH_SOFTWARE, output, evidence, suggest)
    
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
        suggest = "No suggestions"
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_VERSION_IN_METADATA
        suggest = constants.SUGGEST_NO_VERSION_IN_METADATA
        
    check = ch.Check(constants.INDICATORS_DICT['descriptive_metadata'], 'RSFC-03-6', "Version number in metadata", constants.PROCESS_VERSION_IN_METADATA, output, evidence, suggest)

    return check.convert()


def test_has_releases(somef_data):
    if 'releases' not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_RELEASES
        suggest = constants.SUGGEST_NO_RELEASES
    else:
        output = "true"
        evidence = constants.EVIDENCE_RELEASES
        suggest = "No suggestions"
        for item in somef_data['releases']:
            if 'type' in item['result']:
                if item['result']['type'] == 'Release':
                    if 'name' in item['result']:
                        evidence += f'\n\t- {item["result"]["name"]}'
                    elif 'tag' in item['result']:
                        evidence += f'\n\t- {item["result"]["tag"]}'
                    else:
                        evidence += f'\n\t- {item["result"]["url"]}'
                        
    check = ch.Check(constants.INDICATORS_DICT['has_releases'], 'RSFC-03-1', "Software has releases", constants.PROCESS_RELEASES, output, evidence, suggest)

    return check.convert()
    
    
def test_release_id_and_version(somef_data):
    if 'releases' not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_RELEASES
        suggest = constants.SUGGEST_NO_RELEASES
    else:
        results = somef_data['releases']
        for item in results:
            if item['result']['url'] and item['result']['tag']:
                output = "true"
                evidence = constants.EVIDENCE_RELEASE_ID_AND_VERSION
                suggest = "No suggestions"
            else:
                output = "false"
                evidence = constants.EVIDENCE_NO_RELEASE_ID_AND_VERSION
                suggest = constants.SUGGEST_NO_RELEASE_ID_AND_VERSION
                break
                
    check = ch.Check(constants.INDICATORS_DICT['has_releases'], 'RSFC-03-2', "Releases have an id and version number", constants.PROCESS_RELEASE_ID_VERSION, output, evidence, suggest)
    
    return check.convert()


def test_semantic_versioning_standard(somef_data):
    
    if 'releases' not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_RELEASES
        suggest = constants.SUGGEST_NO_RELEASES
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
                    suggest = constants.SUGGEST_NO_VERSIONING_STANDARD
                    break
        
        if output == "true":
            evidence = constants.EVIDENCE_VERSIONING_STANDARD
            suggest = "No suggestions"
                
    check = ch.Check(constants.INDICATORS_DICT['versioning_standards_use'], 'RSFC-03-3', "Release versions follow a community established convention", constants.PROCESS_SEMANTIC_VERSIONING, output, evidence, suggest)
    
    return check.convert()
        
    
def test_version_scheme(somef_data):
    if 'releases' not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_RELEASES
        suggest = constants.SUGGEST_NO_RELEASES
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
                    evidence = constants.EVIDENCE_NO_IDENTIFIER_SCHEME_COMPLIANT
                    suggest = constants.SUGGEST_NO_IDENTIFIER_SCHEME_COMPLIANT
                else:
                    output = "true"
                    
        if output == "true":
            evidence = constants.EVIDENCE_IDENTIFIER_SCHEME_COMPLIANT
            suggest = "No suggestions"
        
    check = ch.Check(constants.INDICATORS_DICT['has_releases'], 'RSFC-03-4', "Release identifiers follow the same scheme", constants.PROCESS_VERSION_SCHEME, output, evidence, suggest)
    
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
        suggest = None
    elif version == latest_release:
        output = "true"
        evidence = constants.EVIDENCE_RELEASE_CONSISTENCY
        suggest = "No suggestions"
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_RELEASE_CONSISTENCY
        suggest = constants.SUGGEST_NO_RELEASE_CONSISTENCY
        
        
    check = ch.Check(constants.INDICATORS_DICT['has_releases'], 'RSFC-03-5', "Last release consistency", constants.PROCESS_RELEASE_CONSISTENCY, output, evidence, suggest)
    
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
        suggest = "No suggestions"
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_METADATA_EXISTS
        suggest = constants.SUGGEST_NO_METADATA_FILES
        
        missing_metadata = [key for key, value in metadata_files.items() if not value]
        missing_metadata_txt = ', '.join(missing_metadata)
        
        evidence += missing_metadata_txt
    
    
    check = ch.Check(constants.INDICATORS_DICT['descriptive_metadata'], 'RSFC-04-1', "Metadata exists", constants.PROCESS_METADATA_EXISTS, output, evidence, suggest)
    
    return check.convert()


def test_readme_exists(somef_data):
    if 'readme_url' in somef_data:
        output = "true"
        evidence = constants.EVIDENCE_DOCUMENTATION_README
        suggest = "No suggestions"
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_DOCUMENTATION_README
        suggest = constants.SUGGEST_NO_README
        
    check = ch.Check(constants.INDICATORS_DICT['software_has_documentation'], 'RSFC-04-2', "There is a README", constants.PROCESS_README, output, evidence, suggest)
    
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
        suggest = "No suggestions"
    elif title and not desc:
        output = "false"
        evidence = constants.EVIDENCE_NO_DESCRIPTION
        suggest = constants.SUGGEST_NO_DESCRIPTION
    elif desc and not title:
        output = "false"
        evidence = constants.EVIDENCE_NO_TITLE
        suggest = constants.SUGGEST_NO_TITLE
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_TITLE_AND_DESCRIPTION
        suggest = constants.SUGGEST_NO_TITLE_DESCRIPTION
        
        
    check = ch.Check(constants.INDICATORS_DICT['descriptive_metadata'], 'RSFC-04-3', "There are title and description", constants.PROCESS_TITLE_DESCRIPTION, output, evidence, suggest)
    
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
        suggest = "No suggestions"
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_DESCRIPTIVE_METADATA
        suggest = constants.SUGGEST_NO_DESCRIPTIVE_METADATA
        
        missing_metadata = [key for key, value in metadata.items() if not value]
        missing_metadata_txt = ', '.join(missing_metadata)
        
        evidence += missing_metadata_txt
        
    check = ch.Check(constants.INDICATORS_DICT['descriptive_metadata'], 'RSFC-04-4', "Software has descriptive metadata", constants.PROCESS_DESCRIPTIVE_METADATA, output, evidence, suggest)
    
    return check.convert()
        
        

def test_codemeta_exists(codemeta_data):
    if codemeta_data != None:
        output = "true"
        evidence = constants.EVIDENCE_METADATA_CODEMETA
        suggest = "No suggestions"
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_METADATA_CODEMETA
        suggest = constants.SUGGEST_NO_CODEMETA
    
    check = ch.Check(constants.INDICATORS_DICT['descriptive_metadata'], 'RSFC-04-5', "There is a codemeta file", constants.PROCESS_CODEMETA, output, evidence, suggest)
    
    return check.convert()

################################################### FRSM_05 ###################################################

def test_repo_status(somef_data):
    if 'repository_status' in somef_data:
        output = "true"
        evidence = constants.EVIDENCE_REPO_STATUS
        suggest = "No suggestions"
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_REPO_STATUS
        suggest = constants.SUGGEST_NO_REPO_STATUS
        
        
    check = ch.Check(constants.INDICATORS_DICT['version_control_use'], 'RSFC-05-1', "There is a repostatus badge", constants.PROCESS_REPO_STATUS, output, evidence, suggest)
    
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
        suggest = "No suggestions"
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_CONTACT_INFO
        suggest = constants.SUGGEST_NO_CONTACT_INFO
        
        missing_sources = [key for key, value in sources.items() if not value]
        missing_sources_txt = ', '.join(missing_sources)
        
        evidence += missing_sources_txt
        
    check = ch.Check(constants.INDICATORS_DICT['software_has_documentation'], 'RSFC-05-2', "There is contact and/or support metadata", constants.PROCESS_CONTACT_SUPPORT_DOCUMENTATION, output, evidence, suggest)
    
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
        suggest = constants.SUGGEST_NO_README_AND_READTHEDOCS
    else:
        evidence = constants.EVIDENCE_DOCUMENTATION + sources
        output = "true"
        suggest = "No suggest"
        
        
    check = ch.Check(constants.INDICATORS_DICT['software_has_documentation'], 'RSFC-05-3', "Software documentation", constants.PROCESS_DOCUMENTATION, output, evidence, suggest)
    
    return check.convert()

################################################### FRSM_06 ###################################################

def test_authors(somef_data, codemeta_data, cff_data):
    
    if 'authors' in somef_data:
        evidence = constants.EVIDENCE_AUTHORS
        output = "true"
        suggest = "No suggestions"
    elif codemeta_data != None and codemeta_data["author"] != None:
        output = "true"
        evidence = constants.EVIDENCE_AUTHORS
        suggest = "No suggestions"
    elif cff_data != None and cff_data["authors"] != None:
        output = "true"
        evidence = constants.EVIDENCE_AUTHORS
        suggest = "No suggestions"
    else:
        evidence = constants.EVIDENCE_NO_AUTHORS
        output = "false"
        suggest = constants.SUGGEST_NO_AUTHORS

        
    check = ch.Check(constants.INDICATORS_DICT['descriptive_metadata'], 'RSFC-06-1', "Authors are declared", constants.PROCESS_AUTHORS, output, evidence, suggest)
    
    return check.convert()


def test_contributors(somef_data, codemeta_data):
    
    if 'contributors' in somef_data:
        output = "true"
        evidence = constants.EVIDENCE_CONTRIBUTORS
        suggest = "No suggestions"
    elif codemeta_data != None and codemeta_data["contributor"] != None:
        output = "true"
        evidence = constants.EVIDENCE_CONTRIBUTORS
        suggest = "No suggestions"
    else:
        evidence = constants.EVIDENCE_NO_CONTRIBUTORS
        output = "false"
        suggest = constants.SUGGEST_NO_CONTRIBUTORS
        
    check = ch.Check(constants.INDICATORS_DICT['descriptive_metadata'], 'RSFC-06-2', "Contributors are declared", constants.PROCESS_CONTRIBUTORS, output, evidence, suggest)
    
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
        suggest = "No suggestions"
    elif author_orcids_codemeta:
        output = "true"
        evidence = constants.EVIDENCE_AUTHOR_ORCIDS_CODEMETA
        suggest = "No suggestions"
    elif author_orcids_cff:
        output = "true"
        evidence = constants.EVIDENCE_AUTHOR_ORCIDS_CFF
        suggest = "No suggestions"
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_AUTHOR_ORCIDS
        suggest = constants.SUGGEST_NO_AUTHOR_ORCIDS
        
    check = ch.Check(constants.INDICATORS_DICT['descriptive_metadata'], 'RSFC-06-3', "Authors have an ORCID", constants.PROCESS_AUTHOR_ORCIDS, output, evidence, suggest)
    
    return check.convert()


def test_author_roles(codemeta_data):
    
    if codemeta_data != None:
        if codemeta_data["author"] != None:
            author_roles = rsfc_helpers.subtest_author_roles(codemeta_data["author"])
            
            if all(value is not None for value in author_roles.values()):
                output = "true"
                evidence = constants.EVIDENCE_AUTHOR_ROLES
                suggest = "No suggestions"
            else:
                output = "false"
                evidence = constants.EVIDENCE_NO_ALL_AUTHOR_ROLES
                suggest = constants.SUGGEST_NO_ALL_AUTHOR_ROLES
        else:
            output = "false"
            evidence = constants.EVIDENCE_NO_AUTHORS_IN_CODEMETA
            suggest = constants.SUGGEST_NO_AUTHORS_IN_CODEMETA
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_CODEMETA_FOUND
        suggest = constants.SUGGEST_NO_CODEMETA
        
    check = ch.Check(constants.INDICATORS_DICT['descriptive_metadata'], 'RSFC-06-4', "Authors have roles", constants.PROCESS_AUTHOR_ROLES, output, evidence, suggest)
    
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
        suggest = "No suggestions"
    elif citation and not readme:
        output = "true"
        evidence = constants.EVIDENCE_IDENTIFIER_IN_CITATION
        suggest = "No suggestions"
    elif citation and readme:
        output = "true"
        evidence = constants.EVIDENCE_IDENTIFIER_IN_README_AND_CITATION
        suggest = "No suggestions"
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_IDENTIFIER_IN_README_OR_CITATION
        suggest = constants.SUGGEST_NO_IDENTIFIER_IN_README_OR_CITATION
        
        
    check = ch.Check(constants.INDICATORS_DICT['persistent_and_unique_identifier'], 'RSFC-07-1', "There is an identifier in README or CITATION.cff", constants.PROCESS_IDENTIFIER_IN_README_CITATION, output, evidence, suggest)
    
    return check.convert()


def test_identifier_resolves_to_software(somef_data, codemeta_data, cff_data, repo_url):
    
    output = "false"
    evidence = constants.EVIDENCE_NO_IDENTIFIER_FOUND
    suggest = constants.SUGGEST_NO_IDENTIFIER
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
                suggest = "No suggestions"
            else:
                output = "false"
                evidence = constants.EVIDENCE_DOI_NO_LINK_BACK_TO_REPO
                suggest = constants.SUGGEST_DOI_NO_LINK_BACK_TO_REPO
                
        except requests.RequestException:
            output = "false"
            evidence = constants.EVIDENCE_NO_RESOLVE_DOI_IDENTIFIER
            suggest = constants.SUGGEST_IDENTIFIER_NO_RESOLVE


    check = ch.Check(constants.INDICATORS_DICT['persistent_and_unique_identifier'], 'RSFC-07-2', "Software identifier resolves to software", constants.PROCESS_ID_RESOLVES_TO_SOFTWARE, output, evidence, suggest)
    
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
        suggest = "No suggestions"
    elif swh:
        output = "true"
        evidence = constants.EVIDENCE_SOFTWARE_HERITAGE_BADGE
        suggest = "No suggestions"
    elif zenodo:
        output = "true"
        evidence = constants.EVIDENCE_ZENODO_DOI
        suggest = "No suggestions"
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_ZENODO_DOI_OR_SOFTWARE_HERITAGE
        suggest = constants.SUGGEST_ARCHIVE_SOFTWARE
        
        
    check = ch.Check(constants.INDICATORS_DICT['archived_in_software_heritage'], 'RSFC-08-1', "Metadata record in Software Heritage or Zenodo", constants.PROCESS_ZENODO_SOFTWARE_HERITAGE, output, evidence, suggest)
    
    return check.convert()

################################################### FRSM_09 ###################################################

def test_is_github_repository(repo_url):

    if 'github.com' in repo_url or 'gitlab.com' in repo_url:
        response = requests.head(repo_url, allow_redirects=True, timeout=5)
        if response.status_code == 200:
            output = "true"
            evidence = constants.EVIDENCE_IS_IN_GITHUB_OR_GITLAB
            suggest = "No suggestions"
        elif response.status_code == 404:
            output = "false"
            evidence = constants.EVIDENCE_NO_RESOLVE_GITHUB_OR_GITLAB_URL
            suggest = "No suggestions"
        else:
            output = "error"
            evidence = 'Connection error'
            suggest = "No suggestions"
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_GITHUB_OR_GITLAB_URL
        suggest = "No suggestions"
    
    check = ch.Check(constants.INDICATORS_DICT['version_control_use'], 'RSFC-09-1', "Repository is from Github/Gitlab", constants.PROCESS_IS_GITHUB_OR_GITLAB_REPOSITORY, output, evidence, suggest)
    
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
        suggest = "No suggestions"
    elif article_citation:
        output = "true"
        evidence = constants.EVIDENCE_CITATION_TO_ARTICLE
        suggest = "No suggestions"
    elif referencePub:
        output = "true"
        evidence = constants.EVIDENCE_REFERENCE_PUBLICATION
        suggest = "No suggestions"
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_REFERENCE_PUBLICATION_OR_CITATION_TO_ARTICLE
        suggest = constants.SUGGEST_NO_REFPUB_OR_ARTICLE
        
        
    check = ch.Check(constants.INDICATORS_DICT['software_has_citation'], 'RSFC-12-1', "There is an article citation or reference publication", constants.PROCESS_REFERENCE_PUBLICATION, output, evidence, suggest)
    
    return check.convert()

################################################### FRSM_13 ###################################################

def test_dependencies_declared(somef_data):
    if 'requirements' not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_DEPENDENCIES
        suggest = constants.SUGGEST_NO_DEPENDENCIES
    else:
        output = "true"
        evidence = constants.EVIDENCE_DEPENDENCIES
        suggest = "No suggestions"
        
        for item in somef_data['requirements']:
            if 'source' in item:
                if item['source'] not in evidence:
                    evidence += f'\n\t- {item["source"]}'

    check = ch.Check(constants.INDICATORS_DICT['requirements_specified'], 'RSFC-13-1', "Dependencies are declared", constants.PROCESS_REQUIREMENTS, output, evidence, suggest)
    
    return check.convert()


def test_installation_instructions(somef_data):
    if 'installation' in somef_data:
        output = "true"
        evidence = constants.EVIDENCE_INSTALLATION
        suggest = "No suggestions"
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_INSTALLATION
        suggest = constants.SUGGEST_NO_INSTALL_INSTRUCTIONS
        
    check = ch.Check(constants.INDICATORS_DICT['software_has_documentation'], 'RSFC-13-2', "There are installation instructions", constants.PROCESS_INSTALLATION, output, evidence, suggest)
    
    return check.convert()


def test_dependencies_have_version(somef_data):
    if 'requirements' not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_DEPENDENCIES
        suggest = constants.SUGGEST_NO_DEPENDENCIES
    else:
        output = "true"
        evidence = constants.EVIDENCE_DEPENDENCIES_VERSION
        suggest = "No suggestions"
        for item in somef_data['requirements']:
            if 'README' not in item['source'] and "version" in item["result"]:
                if item["result"]["version"]:
                    continue
            else:
                output = "false"
                evidence = constants.EVIDENCE_NO_DEPENDENCIES_VERSION
                suggest = constants.SUGGEST_NO_DEPENDENCIES_VERSION
                break
    
    check = ch.Check(constants.INDICATORS_DICT['requirements_specified'], 'RSFC-13-3', "Dependencies have version numbers", constants.PROCESS_DEPENDENCIES_VERSION, output, evidence, suggest)
    
    return check.convert()


def test_dependencies_in_machine_readable_file(somef_data):
    if 'requirements' not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_DEPENDENCIES
        suggest = constants.SUGGEST_NO_DEPENDENCIES
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_DEPENDENCIES_MACHINE_READABLE_FILE
        suggest = constants.SUGGEST_NO_MACHINE_READABLE_DEPENDENCIES
        
        for item in somef_data['requirements']:
            if item['source'] and 'README' not in item['source']:
                output = "true"
                evidence = constants.EVIDENCE_DEPENDENCIES_MACHINE_READABLE_FILE
                suggest = "No suggestions"
                break
            
    check = ch.Check(constants.INDICATORS_DICT['requirements_specified'], 'RSFC-13-4', "There is a dependencies machine-readable file", constants.PROCESS_DEPENDENCIES_MACHINE_READABLE_FILE, output, evidence, suggest)
    
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
            suggest = "No suggestions"
        else:
            output = "false"
            evidence = constants.EVIDENCE_NO_TESTS
            suggest = constants.SUGGEST_NO_TESTS
    else:
        output = "error"
        evidence = None
        suggest = constants.SUGGEST_NO_TESTS
            
    check = ch.Check(constants.INDICATORS_DICT['software_has_tests'], 'RSFC-14-1', "Presence of tests in repository", constants.PROCESS_TESTS, output, evidence, suggest)
    
    return check.convert()


def test_github_action_tests(somef_data):
    sources = ''
    
    if 'continuous_integration' not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_WORKFLOWS
        suggest = constants.SUGGEST_NO_WORKFLOWS
        
    else:
        for item in somef_data['continuous_integration']:
            if item['result']['value'] and ('.github/workflows' in item['result']['value'] or '.gitlab-ci.yml' in item['result']['value']):
                if 'test' in item['result']['value'] or 'tests' in item['result']['value']:
                    sources += f'\t\n- {item["result"]["value"]}'
                    
    if sources:
        output = "true"
        evidence = constants.EVIDENCE_AUTOMATED_TESTS + sources
        suggest = "No suggestions"
        
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_AUTOMATED_TESTS
        suggest = constants.SUGGEST_NO_TEST_ACTIONS
        
        
    check = ch.Check(constants.INDICATORS_DICT['repository_workflows'], 'RSFC-14-2', "There are actions to automate tests", constants.PROCESS_AUTOMATED_TESTS, output, evidence, suggest)
    
    return check.convert()

################################################### FRSM_15 ###################################################

def test_has_license(somef_data):
    if 'license' not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_LICENSE
        suggest = constants.SUGGEST_NO_LICENSE
    else:
        output = "true"
        evidence = constants.EVIDENCE_LICENSE
        suggest = "No suggestions"
        for item in somef_data['license']:
            if 'source' in item:
                evidence += f'\n\t- {item["source"]}'
                
    check = ch.Check(constants.INDICATORS_DICT['software_has_license'], 'RSFC-15-1', "Software has license", constants.PROCESS_LICENSE, output, evidence, suggest)
    
    return check.convert()


def test_license_spdx_compliant(somef_data):
    output = "false"
    evidence = None
    if 'license' not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_LICENSE
        suggest = constants.SUGGEST_NO_LICENSE
    else:
        for item in somef_data['license']:
            if 'result' in item and 'spdx_id' in item['result']:
                if item['result']['spdx_id'] in constants.SPDX_LICENSE_WHITELIST:
                    output = "true"
                else:
                    output = "false"
                    evidence = constants.EVIDENCE_NO_SPDX_COMPLIANT
                    suggest = constants.SUGGEST_NO_LICENSE_SPDX
                    break
        
        if output == "true":
            evidence = constants.EVIDENCE_SPDX_COMPLIANT
            suggest = "No suggestions"
        elif output == "false" and evidence == None:
            evidence = constants.EVIDENCE_LICENSE_NOT_CLEAR
            suggest = "No suggestions"
            
    check = ch.Check(constants.INDICATORS_DICT['software_has_license'], 'RSFC-15-2', "License is SPDX compliant", constants.PROCESS_LICENSE_SPDX_COMPLIANT, output, evidence, suggest)
    
    return check.convert()


'''def test_license_information_provided(somef_data):
    
    if 'license' not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_LICENSE
        suggest = constants.SUGGEST_NO_LICENSE
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_LICENSE_INFORMATION_PROVIDED
        suggest = constants.SUGGEST_NO_LICENSE_INFO
        for item in somef_data['license']:
            if 'source' in item:
                if 'README' in item['source']:
                    output = "true"
                    evidence = constants.EVIDENCE_LICENSE_INFORMATION_PROVIDED
                    suggest = "No suggestions"
                    
                
    check = ch.Check(constants.INDICATORS_DICT['software_has_license'], 'RSFC-15-3', "License information is provided", constants.PROCESS_LICENSE_INFORMATION_PROVIDED, output, evidence, suggest)
    
    return check.convert()'''

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
        suggest = "No suggestions"
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_LICENSE_INFO_IN_METADATA
        suggest = constants.SUGGEST_NO_LICENSE_INFO_METADATA
        
        missing_license_info= [key for key, value in license_info.items() if not value]
        missing_license_info_txt = ', '.join(missing_license_info)
        
        evidence += missing_license_info_txt
        
        
    check = ch.Check(constants.INDICATORS_DICT['software_has_license'], 'RSFC-16-1', "License referenced in metadata files", constants.PROCESS_LICENSE_INFO_IN_METADATA_FILES, output, evidence, suggest)
    
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
            suggest = "No suggestions"
        else:
            output = "false"
            evidence = constants.EVIDENCE_NO_COMMITS
            suggest = constants.SUGGEST_NO_COMMITS
            
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_REPO_STATUS
        suggest = constants.SUGGEST_NO_ACTIVE_REPO
        
        
    check = ch.Check(constants.INDICATORS_DICT['version_control_use'], 'RSFC-17-1', "Repository active", constants.PROCESS_REPO_ENABLED_AND_COMMITS, output, evidence, suggest)
    
    return check.convert()


def test_commit_history(gh):

    commits = gh.commits
    
    if commits != []:
        output = "true"
        evidence = constants.EVIDENCE_COMMITS
        suggest = "No suggestions"
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_COMMITS
        suggest = constants.SUGGEST_NO_COMMITS
        
    check = ch.Check(constants.INDICATORS_DICT['version_control_use'], 'RSFC-17-2', "Commit history", constants.PROCESS_COMMITS_HISTORY, output, evidence, suggest)
    
    return check.convert()

def test_commits_linked_issues(gh):
    
    commits = gh.commits
    issues = gh.issues

    if commits == [] or issues == []:
        output = "false"
        evidence = constants.EVIDENCE_NOT_ENOUGH_ISSUES_COMMITS_INFO
        suggest = constants.SUGGEST_NO_COMMITS_OR_ISSUES
    else:
        linked = rsfc_helpers.cross_check_any_issue(issues, commits)
        
        if linked:
            output = "true"
            evidence = constants.EVIDENCE_COMMITS_LINKED_TO_ISSUES
            suggest = "No suggestions"
        else:
            output = "false"
            evidence = constants.EVIDENCE_NO_COMMITS_LINKED_TO_ISSUES
            suggest = constants.SUGGEST_NO_ISSUES_LINK_COMMITS
            

    check = ch.Check(constants.INDICATORS_DICT['version_control_use'], 'RSFC-17-3', "Commits are linked to issues", constants.PROCESS_COMMITS_LINKED_TO_ISSUES, output, evidence, suggest)
    
    return check.convert()


################################################### MISC ###################################################


def test_has_citation(somef_data):
    if 'citation' not in somef_data:
            output = "false"
            evidence = constants.EVIDENCE_NO_CITATION
            suggest = constants.SUGGEST_NO_CITATION
    else:
        output = "true"
        evidence = constants.EVIDENCE_CITATION
        suggest = "No suggestions"
        for item in somef_data['citation']:
            if 'source' in item:
                if item['source'] not in evidence:
                    evidence += f'\n\t- {item["source"]}'
        
    check = ch.Check(constants.INDICATORS_DICT['software_has_citation'], 'RSFC-18-1', "Repository has citation", constants.PROCESS_CITATION, output, evidence, suggest)
    
    return check.convert()


def test_repository_workflows(somef_data):

    if 'continuous_integration' not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_WORKFLOWS
        suggest = constants.SUGGEST_NO_WORKFLOWS
    else:
        output = "true"
        evidence = constants.EVIDENCE_WORKFLOWS
        suggest = "No suggestions"
    
        for item in somef_data['continuous_integration']:
            evidence += f'\n\t- {item["result"]["value"]}'

    check = ch.Check(constants.INDICATORS_DICT['repository_workflows'], 'RSFC-19-1', "Repository has workflows", constants.PROCESS_WORKFLOWS, output, evidence, suggest)
    
    return check.convert()


def test_has_issue_tracker(somef_data):
    
    if "issue_tracker" not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_ISSUE_TRACKER
        suggest = constants.SUGGEST_NO_ISSUE_TRACKER
    else:
        output = "true"
        evidence = constants.EVIDENCE_ISSUE_TRACKER
        suggest = "No suggestions"
        
    check = ch.Check(constants.INDICATORS_DICT['support_issue_tracking'], 'RSFC-20-1', "Repository has an issue tracker", constants.PROCESS_ISSUE_TRACKER, output, evidence, suggest)
    
    return check.convert()
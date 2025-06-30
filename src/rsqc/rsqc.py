from somef import somef_cli
from jinja2 import Environment, FileSystemLoader
from datetime import datetime, timezone
import json
import base64
import regex as re
import requests
import urllib
import os
from rsqc.utils import constants
from rsqc.model import check as ch
from rsqc.model import assessedSoftware as soft

#################################### Auxs Functions ########################################


def _somef_assessment(repo_url, threshold):
    
    repo_data = somef_cli.cli_get_data(threshold=threshold,
                                    ignore_classifiers=True,
                                    repo_url=repo_url,
                                    readme_only=False)
        
    repo_data = json.loads(json.dumps(repo_data.results))
    
    #Guardar somef output
    os.makedirs('./outputs', exist_ok=True)
    with open('./outputs/somef_assessment.json', 'w', encoding='utf-8') as f:
        json.dump(repo_data, f, indent=4, ensure_ascii=False)
    
    return repo_data


def _get_github_api_url(repo_url):
    parsed_url = urllib.parse.urlparse(repo_url)
    path_parts = parsed_url.path.strip("/").split("/")
    if len(path_parts) < 2:
        raise ValueError("Error when getting Github API URL")
    owner, repo = path_parts[-2], path_parts[-1]
    
    url = f"https://api.github.com/repos/{owner}/{repo}"
    
    return url


def _decode_github_content(content_json):
    encoded_content = content_json.get('content', '')
    encoding = content_json.get('encoding', '')

    if encoding == 'base64':
        return base64.b64decode(encoded_content).decode('utf-8', errors='ignore')
    else:
        return encoded_content


def _resolve_doi_url(doi_badge_url):
    try:
        res = requests.get(doi_badge_url, timeout=5)
        match = re.search(constants.REGEX_ZENODO_URL, res.text)
        if match:
            return True
    except Exception:
        pass
    return False


def _test_codemeta_json(repo_url):
    base_url = _get_github_api_url(repo_url)
    headers = {'Accept': 'application/vnd.github.v3+json'}
    url = base_url + "/contents/codemeta.json"

    response = requests.get(url, headers)

    if response.status_code == 200:
        return True
    elif response.status_code == 404:
        return False
    else:
        raise ConnectionError(f"Error accessing the repository: {response.status_code}")
    
    
def _render_template(repo_url, checks):
    
    data = dict()
    
    sw = soft.AssessedSoftware(repo_url)
    
    data['name'] = sw.software_name
    data['url'] = sw.software_url
    data['version'] = sw.software_version
    data['doi'] = sw.software_id
    data['checks'] = checks
    
    env = Environment(loader=FileSystemLoader("templates"), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template("assessment_schema.json.j2")

    now = datetime.now(timezone.utc)
    data.setdefault("date", str(now.date()))
    data.setdefault("date_iso", now.replace(microsecond=0).isoformat().replace('+00:00', 'Z'))


    rendered = template.render(**data)
    print(rendered)
    return json.loads(rendered)


#################################### Check Functions ########################################
    
    
def check_somef_license(repo_data):
    
    if 'license' not in repo_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_LICENSE
    else:
        output = "true"
        evidence = constants.EVIDENCE_LICENSE
        for item in repo_data['license']:
            if 'source' in item:
                evidence += f'\n\t- {item['source']}'
    
    check = ch.Check(constants.INDICATORS_DICT['software_has_license'], constants.PROCESS_LICENSE, output, evidence)
    
    return check.convert()


def check_somef_documentation(repo_data):
    
    output = "false"
    rtd = False
    readme = False
    
    if 'documentation' in repo_data:
        for item in repo_data['documentation']:
            if 'readthedocs' in item['result']['value']:
                rtd = True
                    
    if 'readme_url' in repo_data:
        readme = True
        
    if rtd and not readme:
        evidence = constants.EVIDENCE_DOCUMENTATION_ONLY_READTHEDOCS
        output = "improvable"
    elif readme and not rtd:
        evidence = constants.EVIDENCE_DOCUMENTATION_ONLY_README
        output = "improvable"
    elif rtd and readme:
        evidence = constants.EVIDENCE_DOCUMENTATION
        output = "true"
    else:
        evidence = constants.EVIDENCE_NO_README_AND_READTHEDOCS
        output = "false"
    
    check = ch.Check(constants.INDICATORS_DICT['software_documentation'], constants.PROCESS_DOCUMENTATION, output, evidence)
    
    return check.convert()
    

def check_somef_citation(repo_data):

    if 'citation' not in repo_data:
        output = False
        evidence = constants.EVIDENCE_NO_CITATION
    else:
        output = True
        evidence = constants.EVIDENCE_CITATION
        for item in repo_data['citation']:
            if 'source' in item:
                if item['source'] not in evidence:
                    evidence += f'\n\t- {item['source']}'
        
    check = ch.Check(constants.INDICATORS_DICT['software_has_citation'], constants.PROCESS_CITATION, output, evidence)
    
    return check.convert()


#TODO ver si se añade otro tipo de validacion con SOMEF
def check_descriptive_metadata(repo_url):

    codemeta = _test_codemeta_json(repo_url)
    
    if codemeta:
        evidence = constants.EVIDENCE_METADATA_CODEMETA
        output = "true"
    else:
        evidence = constants.EVIDENCE_NO_METADATA_CODEMETA
        output = "false"
        
    check = ch.Check(constants.INDICATORS_DICT['descriptive_metadata'], constants.PROCESS_METADATA, output, evidence)
    
    return check.convert()


def check_persistent_unique_id(repo_url):
    
    base_url = _get_github_api_url(repo_url)
    headers = {'Accept': 'application/vnd.github.v3.raw'}
    
    #Look for DOI in readme
    url = base_url+"/readme"
    
    response = requests.get(url, headers)
    
    if response.status_code == 200:
        content_json = response.json()
        readme = _decode_github_content(content_json)
        pattern = constants.REGEX_ZENODO_BADGE
        match = re.search(pattern, readme)
        if match:
            print(match.group(0))
            if _resolve_doi_url(match.group(0)):
                output = "true"
                evidence = constants.EVIDENCE_DOI_IDENTIFIER
            else:
                output = "not valid"
                evidence = constants.EVIDENCE_NO_RESOLVE_DOI_IDENTIFIER
        else:
            output = "false"
            evidence = constants.EVIDENCE_NO_DOI_IDENTIFIER
    elif response.status_code == 404:
        raise FileNotFoundError("README not found.")
    else:
        raise ConnectionError(f"Error accessing the repository: {response.status_code}")
    
    check = ch.Check(constants.INDICATORS_DICT['persistent_and_unique_identifier'], constants.PROCESS_IDENTIFIER, output, evidence)
    
    return check.convert()
   
   
def check_somef_releases(repo_data):
    
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
                        evidence += f'\n\t- {item['result']['name']}'
                    elif 'tag' in item['result']:
                        evidence += f'\n\t- {item['result']['tag']}'
                    else:
                        evidence += f'\n\t- {item['result']['url']}'
    
    check = ch.Check(constants.INDICATORS_DICT['has_releases'], constants.PROCESS_RELEASES, output, evidence)
    
    return check.convert()


def check_repository_workflows(repo_data):

    if 'continuous_integration' not in repo_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_WORKFLOWS
    else:
        output = "true"
        evidence = constants.EVIDENCE_WORKFLOWS
    
        for item in repo_data['continuous_integration']:
            evidence += f'\n\t- {item['result']['value']}'

    check = ch.Check(constants.INDICATORS_DICT['repository_workflows'], constants.PROCESS_WORKFLOWS, output, evidence)
    
    return check.convert()


def check_version_control_use(repo_url):
    
    base_url = _get_github_api_url(repo_url)
    commit_url = base_url+'/commits'
    branch_url = base_url+'/branches'
    
    headers = {'Accept': 'application/vnd.github.v3.raw'}
    
    #Check commits
    response = requests.get(commit_url, headers)
    
    if response.status_code == 200:
        if isinstance(response.json(), list) and len(response.json()) > 0:
            output = "true"
            evidence = constants.EVIDENCE_COMMITS
        else:
            output = "false"
    elif response.status_code == 404:
        raise FileNotFoundError("README not found.")
    else:
        raise ConnectionError(f"Error accessing the repository: {response.status_code}")
        
            
    #Check branches instead
    if output != "true":
        response = requests.get(branch_url, headers)
        
        if response.status_code == 200:
            if isinstance(response.json(), list) and len(response.json()) >= 1:
                output = "true"
                evidence = constants.EVIDENCE_BRANCHES
        elif response.status_code == 404:
            raise FileNotFoundError("README not found.")
        else:
            raise ConnectionError(f"Error accessing the repository: {response.status_code}")
                
    check = ch.Check(constants.INDICATORS_DICT['version_control_use'], constants.PROCESS_VERSION_CONTROL_USE, output, evidence)
    
    return check.convert()


def check_somef_dependencies(repo_data):

    if 'requirements' not in repo_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_DEPENDENCIES
    else:
        output = "true"
        evidence = constants.EVIDENCE_DEPENDENCIES
        
        for item in repo_data['requirements']:
            if 'source' in item:
                evidence += f'\n\t- {item['source']}'

    check = ch.Check(constants.INDICATORS_DICT['requirements_specified'], constants.PROCESS_REQUIREMENTS, output, evidence)
    
    return check.convert()


def build_assessment(repo_url):
    somef_data = _somef_assessment(repo_url, 0.8)

    checks = [
        check_somef_license(somef_data),
        check_somef_citation(somef_data),
        check_somef_releases(somef_data),
        check_repository_workflows(somef_data),
        check_version_control_use(repo_url),
        check_somef_dependencies(somef_data),
        check_somef_documentation(somef_data),
        check_persistent_unique_id(repo_url),
        check_descriptive_metadata(repo_url)
    ]
    
    results = _render_template(repo_url, checks)
    
    output_path = './outputs/rsqc_assessment.json'

    if os.path.exists(output_path):
        os.remove(output_path)

    with open(output_path, 'w') as f:
        json.dump(results, f, indent=4)

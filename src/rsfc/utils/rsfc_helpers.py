import urllib
from datetime import datetime
import regex as re
import base64
from rsfc.utils import constants
import requests


def get_repo_api_url(repo_url, repo_type):
        parsed_url = urllib.parse.urlparse(repo_url)
        path_parts = parsed_url.path.strip("/").split("/")
        if len(path_parts) < 2:
            raise ValueError("Error when getting repository API URL")

        owner, repo = path_parts[-2], path_parts[-1]

        if repo_type == 'GITHUB':
            url = f"https://api.github.com/repos/{owner}/{repo}"
        elif repo_type == "GITLAB":
            project_path = urllib.parse.quote(f"{owner}/{repo}", safe="")
            url = f"https://gitlab.com/api/v4/projects/{project_path}"
        else:
            raise ValueError("URL not within supported types (Github and Gitlab)")

        return url
  
def get_gitlab_default_branch(base_url, repo_type):
    if repo_type == "GITLAB":
        res = requests.get(base_url)
        res.raise_for_status()
        return res.json().get("default_branch", "main")
    else:
        return None

def decode_github_content(content_json):
    encoded_content = content_json.get('content', '')
    encoding = content_json.get('encoding', '')

    if encoding == 'base64':
        return base64.b64decode(encoded_content).decode('utf-8', errors='ignore')
    else:
        return encoded_content

def subtest_author_and_role(codemeta):
    
    #Follows codemeta standards v2.0 and v3.0
    
    output = "false"
    
    if 'author' in codemeta:
        author_roles = {}
        for item in codemeta['author']:
            type_field = None
            id_field = None
            
            if 'type' in item:
                type_field = 'type'
            elif '@type' in item:
                type_field = '@type'
                
            if 'id' in item:
                id_field = 'id'
            elif '@id' in item:
                id_field = '@id'
                
                
            if type_field != None and id_field != None:
                if item[type_field] == 'Person':
                    if item[id_field] not in author_roles:
                        author_roles[item[id_field]] = None
                elif item[type_field] == 'Role' or item[type_field] == 'schema:Role':
                    if item['schema:author'] in author_roles:
                        if 'roleName' in item:
                            author_roles[item['schema:author']] = item['roleName']
                        elif 'schema:roleName' in item:
                            author_roles[item['schema:author']] = item['schema:roleName']
            else:
                continue
    else:
        evidence = constants.EVIDENCE_NO_AUTHORS_IN_CODEMETA
                        

    if all(value is not None for value in author_roles.values()):
        output = "true"
        evidence = constants.EVIDENCE_AUTHOR_ROLES
    else:
        evidence = constants.EVIDENCE_NO_ALL_AUTHOR_ROLES
        
    return output, evidence

def build_url_pattern(url):
    base_url = url.rsplit('/', 1)[0]
    escaped = re.escape(base_url)
    pattern_str = f"^{escaped}/\\d+$"
    return re.compile(pattern_str)

def get_latest_release(repo_data):
    if 'releases' in repo_data:
        latest_release = None
        latest_date = None
        for item in repo_data['releases']:
            if item['result']['date_published'] and item['result']['tag']:
                dt = item['result']['date_published']
                try:
                    dt = datetime.fromisoformat(dt.rstrip('Z'))
                except ValueError:
                    continue
                
                if latest_release is None or dt > latest_date:
                    latest_release = item['result']['tag']
                    latest_date = dt
    else:
        latest_release = None
                
    if latest_release != None:
        return latest_release
    else:
        return None
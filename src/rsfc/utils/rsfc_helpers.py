from datetime import datetime
import regex as re
import base64
from bs4 import BeautifulSoup
import requests
from rsfc.utils import constants
import requests
from requests.exceptions import RequestException

def decode_github_content(content_json):
    encoded_content = content_json.get('content', '')
    encoding = content_json.get('encoding', '')

    if encoding == 'base64':
        return base64.b64decode(encoded_content).decode('utf-8', errors='ignore')
    else:
        return encoded_content

def subtest_author_roles(authors):
    
    #Follows codemeta standards v2.0 and v3.0
    
    author_roles = {}
    for item in authors:
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
        
    return author_roles


def subtest_author_orcids(file_data):
    
    if "author" in file_data: #Codemeta
        for item in file_data["author"]:
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
                if type_field in item and item[type_field] == "Person":
                    if id_field in item and "https://orcid.org/" in item[id_field]:
                        continue
                    else:
                        return False
    elif "authors" in file_data: #CFF
        for item in file_data["authors"]:
            if "orcid" in item:
                continue
            else:
                return False
    else:
        return False
        
    return True
        

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
    
    
def extract_issue_refs(commits):
    
    issue_regex_compiled = re.compile(constants.REGEX_ISSUE_REF, re.IGNORECASE)
    
    issue_refs = set()
    for commit in commits:
        message = commit.get("commit", {}).get("message", "")
        matches = issue_regex_compiled.findall(message)
        issue_refs.update(matches)
    return issue_refs


def check_issue(issue, issue_refs):

    issue_id = str(issue.get("number") or issue.get("iid"))
    return issue_id in issue_refs


def cross_check_any_issue(issues, commits):
    issue_refs = extract_issue_refs(commits)

    for issue in issues:
        issue_id = str(issue.get("number") or issue.get("iid"))
        if issue_id in issue_refs:
            return True

    return False


def normalize_identifier_url(identifier):

    identifier = identifier.strip()
    lower = identifier.lower()

    #Already normalized
    if lower.startswith("https://doi.org/") or lower.startswith("http://doi.org/"):
        return identifier

    #Raw DOI
    if re.match(constants.DOI_SCHEMA_REGEX, identifier, re.IGNORECASE):
        return f"https://doi.org/{identifier}"

    #DOI prefix
    if lower.startswith("doi:"):
        doi = identifier.split(":", 1)[1].strip()
        return f"https://doi.org/{doi}"

    #Other
    if lower.startswith(("http://", "https://")):
        try:
            resp = requests.head(identifier, allow_redirects=True)
            return resp.url
        except requests.RequestException:
            return identifier

    #Fallback
    return identifier


def landing_page_links_back(lp_html, repo_url):
    
    if not lp_html:
        return False
    
    repo_norm = repo_url.rstrip("/").lower()
    soup = BeautifulSoup(lp_html, "html.parser")

    for a in soup.find_all("a", href=True):
        if repo_norm in a["href"].rstrip("/").lower():
            return True

    for m in soup.find_all("meta"):
        content = (m.get("content") or "").lower()
        if repo_norm in content:
            return True

    return False


def resolve_w3id(url):
    
    if "w3id.org" not in url:
        if "github" in url or "gitlab" in url:
            return url
        else:
            return None
    
    try:
        response = requests.get(
            url,
            allow_redirects=True,
            timeout=10
        )
        return response.url

    except RequestException:
        print("Error resolving the w3id")
        return None
    
 
def remove_git_from_url(url):

    if url.endswith(".git"):
        return url[:-4]

    return url
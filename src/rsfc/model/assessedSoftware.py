import urllib
import requests
from packaging.version import parse

class AssessedSoftware:
    def __init__(self, repo_url):
        self.software_url = repo_url
        base_url = self.get_base_url_github(repo_url)
        self.software_name = self.get_soft_name(base_url)
        self.software_version =self.get_soft_version(base_url)
        self.software_id = None
        
        
    def get_base_url_github(self, repo_url):
        parsed_url = urllib.parse.urlparse(repo_url)
        path_parts = parsed_url.path.strip("/").split("/")
        if len(path_parts) < 2:
            raise ValueError("Error when getting Github API URL")
        owner, repo = path_parts[-2], path_parts[-1]
        
        url = f"https://api.github.com/repos/{owner}/{repo}"
        
        return url
        
        
    def get_soft_name(self, base_url):
        name = base_url.rstrip("/").split("/")[-1]
        return name


    def standarize_version(self, ver):
        return ver.replace('_', '.')


    def get_soft_version(self, base_url):
        url = base_url + '/tags'
        response = requests.get(url)
        tags = response.json()

        if not tags:
            return None

        versions = [self.standarize_version(tag['name']) for tag in tags]
        versions.sort(key=parse, reverse=True)
        return versions[0]

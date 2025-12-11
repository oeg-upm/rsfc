
from urllib.parse import unquote

class AssessedSoftware:
    def __init__(self, repo_url, gh):
        self.url = repo_url
        self.name = self.get_soft_name(gh.api_url)
        self.version = gh.version
        self.id = None
        
        
    def get_soft_name(self, api_url):
        base_url = unquote(api_url)
        name = base_url.rstrip("/").split("/")[-1]
        return name
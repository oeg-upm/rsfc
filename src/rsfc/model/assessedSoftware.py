import urllib
from urllib.parse import unquote
import requests
from datetime import datetime
from rsfc.utils import constants, rsfc_helpers

class AssessedSoftware:
    def __init__(self, repo_url):
        self.url = repo_url
        self.repo_type = self.get_repo_type()
        self.base_url = self.get_repo_base_url()
        self.name = self.get_soft_name()
        self.version = self.get_soft_version()
        self.id = None
        self.repo_branch = rsfc_helpers.get_repo_default_branch(self.base_url)
        
        
    def get_repo_base_url(self):
        parsed_url = urllib.parse.urlparse(self.url)
        path_parts = parsed_url.path.strip("/").split("/")
        if len(path_parts) < 2:
            raise ValueError("Error when parsing repository API URL")

        owner, repo = path_parts[-2], path_parts[-1]

        if self.repo_type == constants.REPO_TYPES[0]:
            url = f"https://api.github.com/repos/{owner}/{repo}"
        elif self.repo_type == constants.REPO_TYPES[1]:
            project_path = urllib.parse.quote(f"{owner}/{repo}", safe="")
            url = f"https://gitlab.com/api/v4/projects/{project_path}"
        else:
            raise ValueError("URL not within supported types (Github and Gitlab)")

        return url
        
        
    def get_soft_name(self):
        base_url = unquote(self.base_url)
        name = base_url.rstrip("/").split("/")[-1]
        return name


    def get_soft_version(self):
        try:
            releases_url = f"{self.base_url}/releases"

            response = requests.get(releases_url)
            response.raise_for_status()
            releases = response.json()

            latest_release = None
            latest_date = None

            for release in releases:
                if self.repo_type == "GITHUB":
                    date_str = release.get("published_at")
                    tag = release.get("tag_name")
                elif self.repo_type == "GITLAB":
                    date_str = release.get("released_at")
                    tag = release.get("tag_name")
                else:
                    raise ValueError("Unsupported repository type")

                if date_str and tag:
                    try:
                        dt = datetime.fromisoformat(date_str.rstrip("Z"))
                    except ValueError:
                        continue

                    if latest_release is None or dt > latest_date:
                        latest_release = tag
                        latest_date = dt

            return latest_release

        except Exception as e:
            print(f"Error fetching releases from {self.repo_type} at {releases_url}: {e}")
            return None


    def get_repo_type(self):
        if "github" in self.url:
            repo_type = constants.REPO_TYPES[0]
        elif "gitlab" in self.url:
            repo_type = constants.REPO_TYPES[1]
            
        return repo_type
import urllib
from urllib.parse import unquote
import requests
from datetime import datetime

class AssessedSoftware:
    def __init__(self, repo_url, repo_type):
        self.software_url = repo_url
        base_url = self.get_repo_base_url(repo_url, repo_type)
        self.software_name = self.get_soft_name(unquote(base_url))
        self.software_version = self.get_soft_version(base_url, repo_type)
        self.software_id = None
        
        
    def get_repo_base_url(self, repo_url, repo_type):
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
        
    '''def get_base_url(self, repo_url, repo_type):
        parsed_url = urllib.parse.urlparse(repo_url)
        path_parts = parsed_url.path.strip("/").split("/")
        if len(path_parts) < 2:
            raise ValueError("Error when getting Github API URL")
        owner, repo = path_parts[-2], path_parts[-1]
        
        url = f"https://api.github.com/repos/{owner}/{repo}"
        
        return url'''
        
        
    def get_soft_name(self, base_url):
        name = base_url.rstrip("/").split("/")[-1]
        return name


    def get_soft_version(self, url, repo_type):
        try:
            releases_url = f"{url}/releases"

            response = requests.get(releases_url)
            response.raise_for_status()
            releases = response.json()

            latest_release = None
            latest_date = None

            for release in releases:
                if repo_type == "GITHUB":
                    date_str = release.get("published_at")
                    tag = release.get("tag_name")
                elif repo_type == "GITLAB":
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
            print(f"Error fetching releases from {repo_type} at {releases_url}: {e}")
            return None



    '''def get_soft_version(self, url):
        try:
            releases_url = f"{url}/releases"
            response = requests.get(releases_url)
            response.raise_for_status()
            releases = response.json()

            latest_release = None
            latest_date = None
            for release in releases:
                date_str = release.get("published_at")
                tag = release.get("tag_name")
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
            print(f"Error fetching releases from GitHub: {e}")
            return None'''



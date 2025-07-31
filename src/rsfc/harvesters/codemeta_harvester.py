import requests

class CodemetaHarvester:
    
    def __init__(self, sw):
        codemeta = self.get_codemeta_file(sw)
        self.codemeta_data = self.harvest_codemeta(codemeta)
        
        
    def get_codemeta_file(self, sw):
        req_url = sw.base_url + '/contents/codemeta.json'
        headers = {
            'Accept': 'application/vnd.github.v3.raw'
        }
        
        try:
            if sw.repo_type == "github":
                req_url = sw.base_url + '/contents/codemeta.json'
                headers = {'Accept': 'application/vnd.github.v3.raw'}
                response = requests.get(req_url, headers=headers)
                response.raise_for_status()
                return response.json()
            elif sw.repo_type == "gitlab":
                project_path_encoded = sw.base_url.split("/projects/")[-1]
                branch = sw.repo_branch or "main"
                req_url = f"https://gitlab.com/api/v4/projects/{project_path_encoded}/repository/files/codemeta.json/raw"
                params = {'ref': branch}
                response = requests.get(req_url, params=params)
                response.raise_for_status()
                return response.json()
            else:
                return None

        except requests.RequestException:
            return None
        
    
    def harvest_codemeta(self, codemeta):
        codemeta_info = {
            "license": None,
            "author": None,
            "contributor": None,
            "identifier": None,
            "referencePublication": None,
            "version": None
        }
        
        if "license" in codemeta:
            codemeta_info["license"] = codemeta["license"]
            
        if "identifier" in codemeta:
            codemeta_info["identifier"] = codemeta["identifier"]
            
        if "referencePublication" in codemeta:
            codemeta_info["referencePublication"] = codemeta["referencePublication"]
            
        if "author" in codemeta:
            codemeta_info["author"] = codemeta["author"]
            
        if "contributor" in codemeta:
            codemeta_info["contributor"] = codemeta["contributor"]
            
        if "version" in codemeta:
            codemeta_info["version"] = codemeta["version"]
            
        return codemeta_info
            
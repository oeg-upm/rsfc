import requests
import yaml

class CFFHarvester:
    
    def __init__(self, sw):
        cff = self.get_cff_file(sw)
        self.cff_info = self.harvest_cff(cff)
    
    
    def get_cff_file(self, sw):
        req_url = sw.base_url + '/contents/CITATION.cff'
        headers = {
            'Accept': 'application/vnd.github.v3.raw'
        }
        
        try:
            if sw.repo_type == "GITHUB":
                req_url = sw.base_url + '/contents/CITATION.cff'
                headers = {'Accept': 'application/vnd.github.v3.raw'}
                response = requests.get(req_url, headers=headers)
                response.raise_for_status()
                return yaml.safe_load(response.text)
            elif sw.repo_type == "GITLAB":
                project_path_encoded = sw.base_url.split("/projects/")[-1]
                branch = sw.repo_branch or "main"
                req_url = f"https://gitlab.com/api/v4/projects/{project_path_encoded}/repository/files/CITATION.cff/raw"
                params = {'ref': branch}
                response = requests.get(req_url, params=params)
                response.raise_for_status()
                return yaml.safe_load(response.text)
            else:
                return None

        except requests.RequestException:
            return None
        
    
    def harvest_cff(self, cff):
        
        cff_info = {
            "license": None,
            "authors": None,
            "version": None,
            "identifiers": None,
            "preferred-citation": None
        }
        
        if "license" in cff:
            cff_info["license"] = cff["license"]
            
        if "authors" in cff:
            cff_info["authors"] = cff["authors"]
            
        if "version" in cff:
            cff_info["version"] = cff["version"]
            
        if "idenfiers" in cff:
            cff_info["identifiers"] = cff["identifiers"]
            
        if "preferred-citation" in cff:
            cff_info["preferred-citation"] = cff["preferred-citation"]
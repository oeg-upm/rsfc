from rsfc.utils import constants
from rsfc.harvesters import somef_harvester as som
from rsfc.harvesters import github_harvester as gt
import json


class ExecutionContext:
    
    def __init__(self, repo, branch, tag, metadata, token, s, mode):
        self.repo = repo
        self.somef_kwargs = {
            "threshold": 0.8,
            "ignore_classifiers": True,
            "readme_only": False,
            "output": "./rsfc_output/somef_assessment.json",
            "pretty": True
        }
        if mode == "local":
            self.evaluated_tests = constants.LOCAL_EXEC_TESTS
            self.somef_kwargs["local_repo"] = self.repo
            self.gh_data = None
        elif mode == "remote":
            self.evaluated_tests = constants.REMOTE_EXEC_TESTS
            self.somef_kwargs["repo_url"] = self.repo
            self.gh_data = gt.GithubHarvester(self.repo, branch, tag, token)
        if metadata == None:
            self.somef_data = self.run_somef(branch, tag, token, s)
        else:
            self.somef_data = self.load_metadata(metadata)
        self.sw_name, self.sw_version = self.get_basic_metadata(self.somef_data)
        self.sw_id = None
    
    
    def run_somef(self, branch, tag, token, s):

        if branch is not None:
            self.somef_kwargs["branch"] = branch
        elif tag is not None:
            self.somef_kwargs["tag"] = tag
            
        somef_data = som.SomefHarvester(self.somef_kwargs, token, s).somef_data
        
        return somef_data
    
    
    def load_metadata(self, md_path):
        try:
            with open(md_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading metadata file at '{md_path}': {e}")
            return {}
    
    
    def get_basic_metadata(self, somef_data):
        name = somef_data.get("name", [])
        version = somef_data.get("version", [])
        
        if name:
            name = name[0].get("result", None)
        if version:
            version = version[0].get("result", None)
        
        if name:
            name = name.get("value", None)
        if version:
            version = version.get("tag", None) or version.get("value", None)
            
        return name, version
    
    
    def get_context(self):
        return {
            "evaluated_tests": self.evaluated_tests,
            "somef_data": self.somef_data,
            "gh_data": self.gh_data,
            "repo_url": self.repo,
            "sw_name": self.sw_name,
            "sw_version": self.sw_version,
            "sw_id": self.sw_id
        }
        
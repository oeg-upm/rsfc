import io
import contextlib
import json
from somef import somef_cli
import os

class SomefHarvester:
    
    def __init__(self, repo_url):
        self.somef_data = self.somef_assessment(repo_url, 0.8)
        

    def somef_assessment(self, repo_url, threshold):
    
        print("Extracting repository metadata with SOMEF...")
        
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            repo_data = somef_cli.cli_get_data(threshold=threshold, ignore_classifiers=True, repo_url=repo_url, readme_only=False)
            
        repo_data = json.loads(json.dumps(repo_data.results))
        
        '''os.makedirs('./rsfc_output/', exist_ok=True)
        with open('./rsfc_output/somef_assessment.json', 'w', encoding='utf-8') as f:
            json.dump(repo_data, f, indent=4, ensure_ascii=False)'''
        
        return repo_data
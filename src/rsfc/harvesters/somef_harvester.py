import io
import contextlib
import json
from somef import somef_cli
import subprocess
import os

class SomefHarvester:
    
    def __init__(self, repo_url, token):
        self.somef_configure(token)
        self.somef_data = self.somef_assessment(repo_url, 0.8)
        
        
    def somef_configure(self, token):
        
        print("Configuring SOMEF...")
        
        if token:
            configure = ["somef", "configure"]
            stdin_data = (
            f"{token}\n" #To deal with the inputs asked by somef configure
            "\n"
            "\n"
            "\n"
            "\n"
            "\n"
            )
        else:
            configure = ["somef", "configure", "-a"]
            stdin_data = None

        try:
            subprocess.run(
                configure,
                input=stdin_data,
                text=True,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError("SOMEF configuration failed") from e

    def somef_assessment(self, repo_url, threshold):
    
        print("Extracting repository metadata with SOMEF...")
        
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            repo_data = somef_cli.cli_get_data(threshold=threshold, ignore_classifiers=True, repo_url=repo_url, readme_only=False)
            
        repo_data = json.loads(json.dumps(repo_data.results))
        
        '''os.makedirs('./rsfc_output/', exist_ok=True)
        with open('./rsfc_output/somef_assessment.json', 'w', encoding='utf-8') as f:
            json.dump(repo_data, f, indent=4, ensure_ascii=False)'''
        
        return repo_data
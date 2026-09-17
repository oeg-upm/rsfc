import io
import json
import os
import contextlib
import subprocess
from rsfc.utils.exceptions import GithubRateLimitExceeded

from somef.somef_cli import run_cli


class SomefHarvester:

    def __init__(self, somef_kwargs, token, s):
        self.somef_configure(token)
        self.somef_data = self.somef_assessment(somef_kwargs, s)
        
        

    def somef_configure(self, token):

        print("Configuring SOMEF...")

        if token:
            configure = ["somef", "configure"]
            stdin_data = (
                f"{token}\n"
                "\n"*10
            )

        else:
            configure = ["somef", "configure", "-a"]
            stdin_data = None
            
        try:
            subprocess.run(configure, input=stdin_data, text=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            raise RuntimeError("SOMEF configuration failed") from e



    def somef_assessment(self, somef_kwargs, s):

        print("Extracting repository metadata with SOMEF...")
        os.makedirs("./rsfc_output/", exist_ok=True)
        
        try:
            with (contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO())):
                run_cli(**somef_kwargs)

        except Exception as e:
            if "Token lacks required permissions or scopes" in str(e):
                raise GithubRateLimitExceeded() from e
            
        if not os.path.exists(somef_kwargs["output"]):
            raise RuntimeError(
                "SOMEF did not generate the expected JSON output"
            )
            
        with open(somef_kwargs["output"], "r", encoding="utf-8") as f:
            somef_data = json.load(f)

        if s:
            output_path = "./rsfc_output/somef_assessment.json"

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(somef_data, f, indent=4)

        return somef_data
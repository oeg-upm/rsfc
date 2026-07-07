import io
import json
import os
import glob
import tempfile
import contextlib
import subprocess

from somef.somef_cli import run_cli


class SomefHarvester:

    def __init__(self, repo_url, branch=None, tag=None, token=None):
        soca_metadata = self.find_soca_metadata(repo_url)

        if soca_metadata:
            print(f"Using existing SOMEF metadata from SOCA: {soca_metadata}")

            with open(soca_metadata, "r", encoding="utf-8") as f:
                self.somef_data = json.load(f)

            return

        print("No SOMEF metadata found in SOCA outputs, running SOMEF...")

        self.somef_configure(token)
        self.somef_data = self.somef_assessment(repo_url=repo_url, branch=branch, tag=tag, threshold=0.8)

    @staticmethod
    def find_soca_metadata(repo_url):
        normalized_repo_url = repo_url.rstrip("/")
        repo_owner, repo_name = normalized_repo_url.rsplit("/", 2)[-2:]

        target = os.environ.get("SQOO_SOCA_TARGET")

        patterns = []

        if target:
            patterns.append(
                f"/app/outputs/soca/{target}/metadata/"
                f"{repo_owner}_{repo_name}_*.json"
            )

        patterns.append(
            f"/app/outputs/soca/{repo_owner}/metadata/"
            f"{repo_owner}_{repo_name}_*.json"
        )

        files = []
        for pattern in patterns:
            files.extend(glob.glob(pattern))

        if not files:
            return None

        return max(files, key=os.path.getmtime)

    def somef_configure(self, token):

        print("Configuring SOMEF...")

        if token:

            configure = ["somef", "configure"]

            stdin_data = (
                f"{token}\n"
                "\n"
                "\n"
                "\n"
                "\n"
                "\n"
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
            subprocess.run(configure, input=stdin_data, text=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            raise RuntimeError("SOMEF configuration failed") from e

    def somef_assessment(self, repo_url, branch=None, tag=None, threshold=0.8):

        print("Extracting repository metadata with SOMEF...")

        os.makedirs("./rsfc_output/", exist_ok=True)

        output_json = "./rsfc_output/somef_assessment.json"

        somef_kwargs = {
            "threshold": threshold,
            "ignore_classifiers": True,
            "repo_url": repo_url,
            "readme_only": False,
            "output": output_json,
            "pretty": True
        }

        if branch is not None:
            somef_kwargs["branch"] = branch

        elif tag is not None:
            somef_kwargs["tag"] = tag

        with (contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO())):

            run_cli(**somef_kwargs)

        if not os.path.exists(output_json):

            raise RuntimeError(
                "SOMEF did not generate the expected JSON output"
            )

        with open(output_json, "r", encoding="utf-8") as f:

            repo_data = json.load(f)

        return repo_data
from rsfc.utils import constants
from rsfc.model import check as ch
import requests
from rsfc.utils.registry import test_registry
from rsfc.harvesters.github_harvester import detect_repo_type

################################################### FRSM_09 ###################################################


@test_registry.register_test("RSFC-09-1", args=["repo_url"])
def test_is_github_repository(repo_url):
    # TODO: change the name of the function?

    try:
        detect_repo_type(repo_url)
        supported = True
    except ValueError:
        supported = False

    if supported:
        response = requests.head(repo_url, allow_redirects=True, timeout=5)
        if response.status_code == 200:
            output = "true"
            evidence = constants.EVIDENCE_IS_IN_GITHUB_OR_GITLAB
            suggest = "N/A"
        elif response.status_code == 404:
            output = "false"
            evidence = constants.EVIDENCE_NO_RESOLVE_GITHUB_OR_GITLAB_URL
            suggest = "N/A"
        else:
            output = "indeterminate"
            evidence = "Connection error"
            suggest = "N/A"
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_GITHUB_OR_GITLAB_URL
        suggest = "N/A"

    check = ch.Check(
        constants.INDICATORS_DICT["version_control_use"],
        "RSFC-09-1",
        "Repository is from Github/Gitlab",
        constants.PROCESS_IS_GITHUB_OR_GITLAB_REPOSITORY,
        output,
        evidence,
        suggest,
    )

    return check.convert()

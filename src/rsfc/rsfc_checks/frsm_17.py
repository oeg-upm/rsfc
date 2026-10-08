from rsfc.utils import constants
from rsfc.model import check as ch
from rsfc.utils import rsfc_helpers
from rsfc.utils.registry import test_registry

################################################### FRSM_17 ###################################################

'''def test_repo_enabled_and_commits(somef_data, gh):

    if 'repository_status' in somef_data and somef_data['repository_status'][0]['result']['value']:
        if '#active' in somef_data['repository_status'][0]['result']['value']:
            repo = True
        else:
            repo = False
    else:
        repo = False

    commits = gh.commits

    if repo:
        if commits:
            output = "true"
            evidence = constants.EVIDENCE_REPO_ENABLED_AND_HAS_COMMITS
            suggest = "N/A"
        else:
            output = "false"
            evidence = constants.EVIDENCE_NO_COMMITS
            suggest = constants.SUGGEST_NO_COMMITS

    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_REPO_STATUS
        suggest = constants.SUGGEST_NO_ACTIVE_REPO


    check = ch.Check(constants.INDICATORS_DICT['project_is_active'], 'RSFC-17-1', "Repository is active", constants.PROCESS_REPO_ENABLED_AND_COMMITS, output, evidence, suggest)

    return check.convert()'''


@test_registry.register_test("RSFC-17-2", args=["gh_data"])
def test_commit_history(gh_data):

    commits = gh_data.commits

    if commits[1] != []:
        output = "true"
        evidence = constants.EVIDENCE_COMMITS + f"\n\t- {commits[0]}"
        suggest = "N/A"
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_COMMITS
        suggest = constants.SUGGEST_NO_COMMITS

    check = ch.Check(constants.INDICATORS_DICT['version_control_use'], 'RSFC-17-2', "Commit history", constants.PROCESS_COMMITS_HISTORY, output, evidence, suggest)

    return check.convert()


@test_registry.register_test("RSFC-17-3", args=["gh_data"])
def test_commits_linked_issues(gh_data):
    commits = gh_data.commits
    issues = gh_data.issues
    commits_list = commits[1]

    if commits_list == [] or issues == []:
        output = "false"
        evidence = constants.EVIDENCE_NOT_ENOUGH_ISSUES_COMMITS_INFO
        suggest = constants.SUGGEST_NO_COMMITS_OR_ISSUES
    else:
        linked_pairs = rsfc_helpers.cross_check_any_issue(issues, commits_list)

        if linked_pairs:
            output = "true"
            suggest = "N/A"

            formatted_pairs = "".join([f"\n\t- {pair}" for pair in linked_pairs])
            evidence = constants.EVIDENCE_COMMITS_LINKED_TO_ISSUES + formatted_pairs
        else:
            output = "false"
            evidence = constants.EVIDENCE_NO_COMMITS_LINKED_TO_ISSUES
            suggest = constants.SUGGEST_NO_ISSUES_LINK_COMMITS


    check = ch.Check(constants.INDICATORS_DICT['version_control_use'], 'RSFC-17-3', "Commits are linked to issues", constants.PROCESS_COMMITS_LINKED_TO_ISSUES, output, evidence, suggest)

    return check.convert()

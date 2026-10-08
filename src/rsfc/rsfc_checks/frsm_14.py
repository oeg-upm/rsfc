from rsfc.utils import constants
from rsfc.model import check as ch
import regex as re
from rsfc.utils.registry import test_registry

################################################### FRSM_14 ###################################################


@test_registry.register_test("RSFC-14-1", args=["gh_data"])
def test_presence_of_tests(gh_data):
    test_evidences = gh_data.tests

    if test_evidences:
        rx = re.compile(r"tests?", re.IGNORECASE)
        sources = ""
        for e in test_evidences:
            path = e["path"]
            path_lower = path.lower()

            if "doc" in path_lower or "docs" in path_lower:
                continue
            if rx.search(path):
                sources += f"\n\t- {path}"

        if sources:
            output = "true"
            evidence = constants.EVIDENCE_TESTS + sources
            suggest = "N/A"
        else:
            output = "false"
            evidence = constants.EVIDENCE_NO_TESTS
            suggest = constants.SUGGEST_NO_TESTS
    else:
        output = "indeterminate"
        evidence = None
        suggest = constants.SUGGEST_NO_TESTS

    check = ch.Check(
        constants.INDICATORS_DICT["software_has_tests"],
        "RSFC-14-1",
        "Presence of tests in repository",
        constants.PROCESS_TESTS,
        output,
        evidence,
        suggest,
    )

    return check.convert()


@test_registry.register_test("RSFC-14-2", args=["somef_data"])
def test_github_action_tests(somef_data):
    sources = ""

    if "continuous_integration" not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_WORKFLOWS
        suggest = constants.SUGGEST_NO_WORKFLOWS

    else:
        for item in somef_data["continuous_integration"]:
            if item["result"]["value"] and (
                ".github/workflows" in item["result"]["value"]
                or ".gitlab-ci.yml" in item["result"]["value"]
            ):
                if any(
                    keyword in item["result"]["value"]
                    for keyword in ["test", "validate", "check"]
                ):
                    sources += f"\n\t- {item['result']['value']}"

    if sources:
        output = "true"
        evidence = constants.EVIDENCE_AUTOMATED_TESTS + sources
        suggest = "N/A"

    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_AUTOMATED_TESTS
        suggest = constants.SUGGEST_NO_TEST_ACTIONS

    check = ch.Check(
        constants.INDICATORS_DICT["repository_workflows"],
        "RSFC-14-2",
        "There are actions to automate tests",
        constants.PROCESS_AUTOMATED_TESTS,
        output,
        evidence,
        suggest,
    )

    return check.convert()


"""def test_has_no_known_bugs(gh_data):
    if len(gh_data.bug_issues) == 0:
        output = "true"
        evidence = constants.EVIDENCE_NO_ISSUES_BUG
        suggest = "N/A"
    else:
        output = "false"
        evidence = constants.EVIDENCE_ISSUES_BUGS
        suggest = constants.SUGGEST_ISSUES_BUGS

    check = ch.Check(constants.INDICATORS_DICT['software_has_no_known_bugs'], 'RSFC-14-3', "Software has no issues tagged as bugs", constants.PROCESS_ISSUES_BUGS, output, evidence, suggest)

    return check.convert()"""

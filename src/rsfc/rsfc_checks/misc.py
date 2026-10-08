from rsfc.utils import constants
from rsfc.model import check as ch
from rsfc.utils.registry import test_registry

################################################### MISC ###################################################


@test_registry.register_test("RSFC-18-1", args=["somef_data"])
def test_has_citation(somef_data):

    if 'citation' not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_CITATION
        suggest = constants.SUGGEST_NO_CITATION
    else:
        output = "true"
        suggest = "N/A"

        sources = set()

        for item in somef_data['citation']:
            if 'source' not in item:
                continue

            source = item['source']

            if isinstance(source, list):
                sources.update(source)
            else:
                sources.add(source)

        formatted_sources = ''.join(f'\n\t- {source}' for source in sorted(sources))
        evidence = constants.EVIDENCE_CITATION + formatted_sources

    check = ch.Check(constants.INDICATORS_DICT['software_has_citation'], 'RSFC-18-1', "Repository has citation", constants.PROCESS_CITATION, output, evidence, suggest)

    return check.convert()


@test_registry.register_test("RSFC-19-1", args=["somef_data"])
def test_repository_workflows(somef_data):

    if 'continuous_integration' not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_WORKFLOWS
        suggest = constants.SUGGEST_NO_WORKFLOWS
    else:
        output = "true"
        evidence = constants.EVIDENCE_WORKFLOWS
        suggest = "N/A"

        for item in somef_data['continuous_integration']:
            evidence += f'\n\t- {item["result"]["value"]}'

    check = ch.Check(constants.INDICATORS_DICT['repository_workflows'], 'RSFC-19-1', "Repository has workflows", constants.PROCESS_WORKFLOWS, output, evidence, suggest)

    return check.convert()


@test_registry.register_test("RSFC-20-1", args=["somef_data"])
def test_has_issue_tracker(somef_data):

    if "issue_tracker" not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_ISSUE_TRACKER
        suggest = constants.SUGGEST_NO_ISSUE_TRACKER
    else:
        for item in somef_data["issue_tracker"]:
            sources = ""
            if "source" in item:
                sources += f"\n\t- {item["source"]}"

        if sources:
            evidence = constants.EVIDENCE_ISSUE_TRACKER_SOURCE + sources
        else:
            evidence = constants.EVIDENCE_ISSUE_TRACKER_NO_SOURCE

        output = "true"
        suggest = "N/A"

    check = ch.Check(constants.INDICATORS_DICT['support_issue_tracking'], 'RSFC-20-1', "Repository has an issue tracker", constants.PROCESS_ISSUE_TRACKER, output, evidence, suggest)

    return check.convert()


@test_registry.register_test("RSFC-21-1", args=["somef_data"])
def test_has_contribution_guidelines(somef_data):
    if "contributing_guidelines" not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_CONTRIBUTION_GUIDELINES
        suggest = constants.SUGGEST_NO_CONTRIBUTION_GUIDELINES
    else:
        output = "true"
        evidence = constants.EVIDENCE_CONTRIBUTION_GUIDELINES
        suggest = "N/A"

        for item in somef_data["contributing_guidelines"]:
            sources = item.get("source", "")

            if isinstance(sources, list):
                sources = ", ".join(str(s) for s in sources)

            if sources:
                evidence += f'\n\t- {sources}'
            else:
                evidence += '\n\t- (source not found)'

    check = ch.Check(constants.INDICATORS_DICT['has_contribution_guidelines'], 'RSFC-21-1', "Repository has contribution guidelines", constants.PROCESS_CONTRIBUTION_GUIDELINES, output, evidence, suggest)

    return check.convert()


@test_registry.register_test("RSFC-22-1", args=["somef_data"])
def test_containerized(somef_data):

    unique_sources = set()

    if "has_build_file" in somef_data and isinstance(somef_data["has_build_file"], list):
        for item in somef_data["has_build_file"]:
            if "source" in item and "result" in item and "format" in item["result"]:
                fmt = str(item["result"]["format"]).lower().strip()

                if fmt in constants.VALID_CONTAINER_FORMATS:
                    sources = item["source"]
                    sources_list = sources if isinstance(sources, list) else [sources]
                    for s in sources_list:
                        if s and str(s).strip():
                            unique_sources.add(str(s).strip())

    if unique_sources:
        output = "true"
        suggest = "N/A"
        formatted_sources = "".join([f"\n\t- {src}" for src in sorted(unique_sources)])
        evidence = constants.EVIDENCE_CONTAINER_FILE + formatted_sources
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_CONTAINER_FILE
        suggest = constants.SUGGEST_NO_CONTAINER_FILE

    check = ch.Check(constants.INDICATORS_DICT['software_is_containerized'], 'RSFC-22-1', "Software is containerized", constants.PROCESS_CONTAINER_FILE, output, evidence, suggest)

    return check.convert()

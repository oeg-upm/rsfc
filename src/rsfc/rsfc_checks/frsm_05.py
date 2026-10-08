from rsfc.utils import constants
from rsfc.model import check as ch
from rsfc.utils.registry import test_registry

################################################### FRSM_05 ###################################################


@test_registry.register_test("RSFC-05-1", args=["somef_data"])
def test_repo_status(somef_data):
    unique_sources = set()

    if 'repository_status' in somef_data and isinstance(somef_data['repository_status'], list):
        for item in somef_data['repository_status']:
            if "source" in item:
                sources = item["source"]
                sources_list = sources if isinstance(sources, list) else [sources]
                for s in sources_list:
                    if s and str(s).strip():
                        unique_sources.add(str(s).strip())

    if unique_sources:
        output = "true"
        suggest = "N/A"

        formatted_sources = "".join([f"\n\t- {src}" for src in sorted(unique_sources)])
        evidence = constants.EVIDENCE_REPO_STATUS + formatted_sources
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_REPO_STATUS
        suggest = constants.SUGGEST_NO_REPO_STATUS

    check = ch.Check(constants.INDICATORS_DICT['version_control_use'], 'RSFC-05-1', "There is a repostatus badge", constants.PROCESS_REPO_STATUS, output, evidence, suggest)

    return check.convert()


@test_registry.register_test("RSFC-05-2", args=["somef_data"])
def test_contact_support_documentation(somef_data):
    unique_sources = set()

    keys_to_check = ['contact', 'support', 'support_channels']

    for key in keys_to_check:
        if key in somef_data and isinstance(somef_data[key], list):
            for item in somef_data[key]:
                if "source" in item:
                    sources = item["source"]
                    sources_list = sources if isinstance(sources, list) else [sources]
                    for s in sources_list:
                        if s and str(s).strip():
                            unique_sources.add(str(s).strip())

    if unique_sources:
        output = "true"
        suggest = "N/A"

        formatted_sources = "".join([f"\n\t- {src}" for src in sorted(unique_sources)])
        evidence = constants.EVIDENCE_CONTACT_INFO + formatted_sources
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_CONTACT_INFO
        suggest = constants.SUGGEST_NO_CONTACT_INFO

    check = ch.Check(constants.INDICATORS_DICT['software_has_documentation'], 'RSFC-05-2', "There is contact and/or support metadata", constants.PROCESS_CONTACT_SUPPORT_DOCUMENTATION, output, evidence, suggest)

    return check.convert()


@test_registry.register_test("RSFC-05-3", args=["somef_data"])
def test_software_documentation(somef_data):
    rtd = False
    readme = False
    sources = set()

    if 'documentation' in somef_data and isinstance(somef_data['documentation'], list):
        for item in somef_data['documentation']:
            if 'result' in item:
                result_val = str(item['result'].get('value', '')).lower()
                result_format = str(item['result'].get('format', '')).lower()

                if 'readthedocs' in result_val or 'readthedocs' in result_format:
                    rtd = True
                    if 'source' in item:
                        source_field = item["source"]
                        sources_list = source_field if isinstance(source_field, list) else [source_field]

                        for s in sources_list:
                            if s and str(s).strip():
                                sources.add(str(s).strip())

    if 'readme_url' in somef_data and isinstance(somef_data['readme_url'], list):
        for item in somef_data['readme_url']:
            if 'result' in item and 'value' in item['result']:
                val = item['result']['value']
                if val and str(val).strip():
                    readme = True
                    sources.add(str(val).strip())

    if not readme and not rtd:
        output = "false"
        evidence = constants.EVIDENCE_NO_README_AND_READTHEDOCS
        suggest = constants.SUGGEST_NO_README_AND_READTHEDOCS
    else:
        output = "true"
        suggest = "N/A"

        formatted_sources = ''.join(f"\n\t- {source}" for source in sorted(sources))
        evidence = constants.EVIDENCE_DOCUMENTATION + formatted_sources

    check = ch.Check(constants.INDICATORS_DICT['software_has_documentation'], 'RSFC-05-3', "Software documentation", constants.PROCESS_DOCUMENTATION, output, evidence, suggest)

    return check.convert()


@test_registry.register_test("RSFC-05-4", args=["somef_data"])
def test_active_communication_channels(somef_data):
    unique_sources = set()

    if "support_channels" in somef_data and isinstance(somef_data["support_channels"], list):
        for item in somef_data["support_channels"]:
            if "source" in item:
                sources = item["source"]
                sources_list = sources if isinstance(sources, list) else [sources]
                for s in sources_list:
                    if s and str(s).strip():
                        unique_sources.add(str(s).strip())

    if unique_sources:
        output = "true"
        suggest = "N/A"

        formatted_sources = "".join([f"\n\t- {src}" for src in sorted(unique_sources)])
        evidence = constants.EVIDENCE_COMMUNICATION_CHANNELS + formatted_sources
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_COMMUNICATION_CHANNELS
        suggest = constants.SUGGEST_NO_COMMUNICATION_CHANNELS

    check = ch.Check(constants.INDICATORS_DICT['has_active_communication_channels'], 'RSFC-05-4', "Software has active commmunication channels", constants.PROCESS_COMMUNICATION_CHANNELS, output, evidence, suggest)

    return check.convert()

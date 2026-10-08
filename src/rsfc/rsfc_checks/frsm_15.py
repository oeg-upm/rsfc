from rsfc.utils import constants
from rsfc.model import check as ch
from rsfc.utils.registry import test_registry

################################################### FRSM_15 ###################################################


@test_registry.register_test("RSFC-15-1", args=["somef_data"])
def test_has_license(somef_data):
    if 'license' not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_LICENSE
        suggest = constants.SUGGEST_NO_LICENSE
    else:
        output = "true"
        evidence = constants.EVIDENCE_LICENSE
        suggest = "N/A"

        for item in somef_data['license']:
            if 'source' in item:
                sources = item["source"]
                if isinstance(sources, list):
                    for s in sources:
                        evidence += f'\n\t- {s}'
                elif isinstance(sources, str) and sources:
                    evidence += f'\n\t- {sources}'

    check = ch.Check(constants.INDICATORS_DICT['software_has_license'], 'RSFC-15-1', "Software has license", constants.PROCESS_LICENSE, output, evidence, suggest)

    return check.convert()


@test_registry.register_test("RSFC-15-2", args=["somef_data"])
def test_license_spdx_compliant(somef_data):
    output = "false"
    evidence = None

    if 'license' not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_LICENSE
        suggest = constants.SUGGEST_NO_LICENSE
    else:
        output = "true"
        suggest = "N/A"
        no_spdx = ""

        evaluated_any = False

        for item in somef_data['license']:
            if 'result' in item and 'spdx_id' in item['result']:
                evaluated_any = True
                spdx_id = item['result']['spdx_id']

                if spdx_id not in constants.SPDX_LICENSE_WHITELIST:
                    if output != "false":
                        output = "false"
                        suggest = constants.SUGGEST_NO_LICENSE_SPDX

                    no_spdx += f"\n\t- {spdx_id}"

        if output == "true" and evaluated_any:
            evidence = constants.EVIDENCE_SPDX_COMPLIANT
        elif output == "false" and no_spdx:
            evidence = constants.EVIDENCE_NO_SPDX_COMPLIANT + no_spdx
        else:
            output = "false"
            evidence = constants.EVIDENCE_LICENSE_NOT_CLEAR
            suggest = "N/A"

    check = ch.Check(constants.INDICATORS_DICT['software_has_license'], 'RSFC-15-2', "License is SPDX compliant", constants.PROCESS_LICENSE_SPDX_COMPLIANT, output, evidence, suggest)

    return check.convert()

'''def test_license_information_provided(somef_data):

    if 'license' not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_LICENSE
        suggest = constants.SUGGEST_NO_LICENSE
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_LICENSE_INFORMATION_PROVIDED
        suggest = constants.SUGGEST_NO_LICENSE_INFO
        for item in somef_data['license']:
            if 'source' in item:
                if 'README' in item['source']:
                    output = "true"
                    evidence = constants.EVIDENCE_LICENSE_INFORMATION_PROVIDED
                    suggest = "N/A"


    check = ch.Check(constants.INDICATORS_DICT['software_has_license'], 'RSFC-15-3', "License information is provided", constants.PROCESS_LICENSE_INFORMATION_PROVIDED, output, evidence, suggest)

    return check.convert()'''

from rsfc.utils import constants
from rsfc.model import check as ch
from rsfc.utils.registry import test_registry

################################################### FRSM_08 ###################################################


@test_registry.register_test("RSFC-08-1", args=["somef_data"])
def test_metadata_record_in_software_heritage(somef_data):
    swh_identifiers = []

    if "identifier" in somef_data:
        for item in somef_data['identifier']:
            if 'result' in item and 'value' in item['result'] and item['result']['value']:
                val = item['result']['value']
                if 'softwareheritage' in val:
                    swh_identifiers.append(val)

    if swh_identifiers:
        output = "true"
        suggest = "N/A"

        formatted_ids = "".join([f"\n\t- {id_val}" for id_val in swh_identifiers])
        evidence = constants.EVIDENCE_SOFTWARE_HERITAGE_BADGE + formatted_ids

    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_SOFTWARE_HERITAGE
        suggest = constants.SUGGEST_ARCHIVE_SOFTWARE

    check = ch.Check(constants.INDICATORS_DICT['archived_in_software_heritage'], 'RSFC-08-1', "Metadata record in Software Heritage", constants.PROCESS_SOFTWARE_HERITAGE, output, evidence, suggest)

    return check.convert()


@test_registry.register_test("RSFC-08-2", args=["somef_data"])
def test_metadata_record_in_zenodo(somef_data):
    zenodo_identifiers = []

    if "identifier" in somef_data:
        for item in somef_data['identifier']:
            if 'result' in item and 'value' in item['result'] and item['result']['value']:
                val = item['result']['value']
                if 'zenodo' in val:
                    zenodo_identifiers.append(val)

    if zenodo_identifiers:
        output = "true"
        suggest = "N/A"

        formatted_ids = "".join([f"\n\t- {id_val}" for id_val in zenodo_identifiers])
        evidence = constants.EVIDENCE_ZENODO_DOI + formatted_ids

    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_ZENODO_DOI
        suggest = constants.SUGGEST_ARCHIVE_SOFTWARE

    check = ch.Check(constants.INDICATORS_DICT['archived_in_scholarly_repository'], 'RSFC-08-2', "Metadata record in scholarly repository", constants.PROCESS_ZENODO, output, evidence, suggest)

    return check.convert()

from rsfc.utils import constants
from rsfc.model import check as ch
import regex as re
import requests
from rsfc.utils.registry import test_registry

################################################### FRSM_01 ###################################################

@test_registry.register_test("RSFC-01-1", args=["somef_data"])
def test_id_presence_and_resolves(somef_data):

    if "identifier" not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_IDENTIFIER_FOUND
        suggest = constants.SUGGEST_NO_IDENTIFIER
    else:
        for item in somef_data["identifier"]:
            sources = item.get("source", [])
            sources_list = sources if isinstance(sources, list) else [sources]

            readme_source = any("README" in source for source in sources_list)

            if not readme_source:
                output = "false"
                evidence = constants.EVIDENCE_NO_IDENTIFIER_FOUND_README
                suggest = constants.SUGGEST_NO_IDENTIFIER_README
            else:
                identifier = item["result"]["value"]

                if (identifier.startswith("http://") or identifier.startswith("https://")):
                    try:
                        response = requests.get(identifier, allow_redirects=True, timeout=10, stream=True)

                        if response.status_code == 200:
                            output = "true"
                            evidence = constants.EVIDENCE_ID_FOUND_AND_RESOLVES.format(id=identifier)
                            suggest = "N/A"

                        else:
                            output = "false"
                            evidence = constants.EVIDENCE_NO_ID_RESOLVE.format(id=identifier)
                            suggest = constants.SUGGEST_IDENTIFIER_NO_RESOLVE

                    except requests.RequestException:
                        output = "indeterminate"
                        evidence = "Something went wrong when trying to resolve the identifier"
                        suggest = None

                else:
                    output = "false"
                    evidence = constants.EVIDENCE_ID_NOT_URL.format(id=identifier)
                    suggest = constants.SUGGEST_IDENTIFIER_NOT_HTTP

    check = ch.Check(constants.INDICATORS_DICT['persistent_and_unique_identifier'], 'RSFC-01-1', "There is an identifier and resolves", constants.PROCESS_IDENTIFIER, output, evidence, suggest)

    return check.convert()


@test_registry.register_test("RSFC-01-3", args=["somef_data"])
def test_id_common_schema(somef_data):
    output = "true"
    evidence = constants.EVIDENCE_ID_COMMON_SCHEMA
    suggest = "N/A"

    compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in constants.ID_SCHEMA_REGEX_LIST]
    failed_identifiers = []
    any_identifier_found = False

    if 'identifier' in somef_data and isinstance(somef_data['identifier'], list):
        for item in somef_data['identifier']:
            if "source" in item and "result" in item and "value" in item["result"]:
                any_identifier_found = True
                value = item['result']['value']

                if value and not any(pattern.match(str(value)) for pattern in compiled_patterns):
                    sources = item['source']
                    sources_str = ", ".join(sources) if isinstance(sources, list) else sources
                    failed_identifiers.append(f"\n\t- Identifier '{value}' found in: {sources_str}")

    if 'citation' in somef_data and isinstance(somef_data['citation'], list):
        for item in somef_data['citation']:
            if "source" in item and "result" in item and "identifier" in item["result"]:
                citation_ids = item["result"]["identifier"]
                citation_ids_list = citation_ids if isinstance(citation_ids, list) else [citation_ids]

                for cid in citation_ids_list:
                    if isinstance(cid, dict) and "value" in cid:
                        any_identifier_found = True
                        value = cid['value']

                        if value and not any(pattern.search(str(value)) for pattern in compiled_patterns):
                            sources = item['source']
                            sources_str = ", ".join(sources) if isinstance(sources, list) else sources
                            failed_identifiers.append(f"\n\t- Identifier '{value}' found in: {sources_str}")

    if not any_identifier_found:
        output = "false"
        evidence = constants.EVIDENCE_NO_IDENTIFIER_FOUND
        suggest = constants.SUGGEST_NO_IDENTIFIER
    elif failed_identifiers:
        output = "false"
        suggest = constants.SUGGEST_IDENTIFIER_SCHEME
        evidence = constants.EVIDENCE_NO_ID_COMMON_SCHEMA + "".join(failed_identifiers)
    else:
        output = "true"
        evidence = constants.EVIDENCE_ID_COMMON_SCHEMA
        suggest = "N/A"

    check = ch.Check(constants.INDICATORS_DICT['persistent_and_unique_identifier'], 'RSFC-01-3', "Software identifier follows a proper schema", constants.PROCESS_ID_PROPER_SCHEMA, output, evidence, suggest)

    return check.convert()


@test_registry.register_test("RSFC-01-2", args=["somef_data"])
def test_id_associated_with_software(somef_data):
    id_locations = {
        'codemeta.json': False,
        'CITATION.cff': False,
        'README.md': False
    }

    if "identifier" in somef_data and isinstance(somef_data['identifier'], list):
        for item in somef_data['identifier']:
            if 'source' in item:
                sources = item["source"]
                sources_list = sources if isinstance(sources, list) else [sources]

                for s in sources_list:
                    if 'README.md' in str(s):
                        id_locations['README.md'] = True
                    if "codemeta.json" in str(s):
                        id_locations["codemeta.json"] = True

    if "citation" in somef_data and isinstance(somef_data['citation'], list):
        for item in somef_data['citation']:
            if "result" in item and "identifier" in item["result"] and item["result"]["identifier"]:
                if 'source' in item:
                    sources = item["source"]
                    sources_list = sources if isinstance(sources, list) else [sources]

                    for s in sources_list:
                        if ".cff" in str(s) or "CITATION.cff" in str(s):
                            id_locations["CITATION.cff"] = True

    if any(id_locations.values()):
        output = "true"
        suggest = "N/A"

        existing_id_locations = [key for key, value in id_locations.items() if value]
        existing_id_locations_txt = ', '.join(sorted(existing_id_locations))
        evidence = constants.EVIDENCE_SOME_ID_ASSOCIATED_WITH_SOFTWARE.format(source=existing_id_locations_txt)

        missing_id_locations = [key for key, value in id_locations.items() if not value]
        if missing_id_locations:
            missing_id_locations_txt = ', '.join(sorted(missing_id_locations))
            evidence += constants.EVIDENCE_MISSING_IDS.format(missing_sources=missing_id_locations_txt)

    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_ID_ASSOCIATED_WITH_SOFTWARE
        suggest = constants.SUGGEST_NO_IDENTIFIER_ASSOCIATED


    check = ch.Check(constants.INDICATORS_DICT['persistent_and_unique_identifier'], 'RSFC-01-2', "There is an identifier associated with the software", constants.PROCESS_ID_ASSOCIATED_WITH_SOFTWARE, output, evidence, suggest)

    return check.convert()

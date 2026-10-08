from rsfc.utils import constants
from rsfc.model import check as ch
import requests
from rsfc.utils import rsfc_helpers
from rsfc.utils.registry import test_registry

################################################### FRSM_07 ###################################################


@test_registry.register_test("RSFC-07-1", args=["somef_data"])
def test_identifier_in_readme_citation(somef_data):
    readme_ids = []
    citation_ids = []

    if "identifier" in somef_data:
        for item in somef_data["identifier"]:
            if "source" in item and "result" in item and "value" in item["result"]:
                sources = item["source"]
                sources_list = sources if isinstance(sources, list) else [sources]

                if any("README" in str(s) for s in sources_list):
                    val = item["result"]["value"]
                    if val:
                        readme_ids.append(val)

    if "citation" in somef_data:
        for item in somef_data["citation"]:
            if "result" in item and "identifier" in item["result"]:
                citations_list = item["result"]["identifier"]

                if isinstance(citations_list, list):
                    for ident in citations_list:
                        if isinstance(ident, dict) and "value" in ident and ident["value"]:
                            citation_ids.append(ident["value"])

    if citation_ids and readme_ids:
        output = "true"
        suggest = "N/A"

        all_ids = readme_ids + citation_ids
        formatted_ids = "".join([f"\n\t- {id_val}" for id_val in all_ids])
        evidence = constants.EVIDENCE_IDENTIFIER_IN_README_AND_CITATION + formatted_ids

    elif citation_ids:
        output = "true"
        suggest = "N/A"

        formatted_ids = "".join([f"\n\t- {id_val}" for id_val in citation_ids])
        evidence = constants.EVIDENCE_IDENTIFIER_IN_CITATION + formatted_ids

    elif readme_ids:
        output = "true"
        suggest = "N/A"

        formatted_ids = "".join([f"\n\t- {id_val}" for id_val in readme_ids])
        evidence = constants.EVIDENCE_IDENTIFIER_IN_README + formatted_ids

    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_IDENTIFIER_IN_README_OR_CITATION
        suggest = constants.SUGGEST_NO_IDENTIFIER_IN_README_OR_CITATION

    check = ch.Check(constants.INDICATORS_DICT['persistent_and_unique_identifier'], 'RSFC-07-1', "There is an identifier in README or CITATION.cff", constants.PROCESS_IDENTIFIER_IN_README_CITATION, output, evidence, suggest)

    return check.convert()


@test_registry.register_test("RSFC-07-2", args=["somef_data", "repo_url"])
def test_identifier_resolves_to_software(somef_data, repo_url):
    output = "false"
    evidence = constants.EVIDENCE_NO_IDENTIFIER_FOUND
    suggest = constants.SUGGEST_NO_IDENTIFIER
    identifier = None
    pause = False

    if "identifier" in somef_data:
        for item in somef_data["identifier"]:
            if "source" in item and "result" in item and "value" in item["result"]:
                sources = item["source"]
                sources_list = sources if isinstance(sources, list) else [sources]

                if any("README" in str(s) or "codemeta.json" in str(s) for s in sources_list):
                    if item['result']['value']:
                        identifier = item['result']['value']
                        pause = True
                        break

    if not pause:
        if "citation" in somef_data:
            for item in somef_data["citation"]:
                if "result" in item and "identifier" in item["result"]:
                    citations_list = item["result"]["identifier"]

                    if isinstance(citations_list, list) and citations_list:
                        first_id = citations_list[0]
                        if isinstance(first_id, dict) and "value" in first_id and first_id["value"]:
                            identifier = first_id["value"]
                            break

    if identifier:
        doi_url = rsfc_helpers.normalize_identifier_url(identifier)
        try:
            resp = requests.get(doi_url, allow_redirects=True, timeout=10)
            html = resp.text

            if rsfc_helpers.landing_page_links_back(html, repo_url):
                output = "true"
                evidence = constants.EVIDENCE_DOI_LINKS_BACK_TO_REPO.format(identifier=identifier)
                suggest = "N/A"
            else:
                output = "false"
                evidence = constants.EVIDENCE_DOI_NO_LINK_BACK_TO_REPO
                suggest = constants.SUGGEST_DOI_NO_LINK_BACK_TO_REPO

        except requests.RequestException:
            output = "false"
            evidence = constants.EVIDENCE_NO_RESOLVE_DOI_IDENTIFIER
            suggest = constants.SUGGEST_IDENTIFIER_NO_RESOLVE

    check = ch.Check(constants.INDICATORS_DICT['persistent_and_unique_identifier'], 'RSFC-07-2', "Software identifier resolves to software", constants.PROCESS_ID_RESOLVES_TO_SOFTWARE, output, evidence, suggest)

    return check.convert()

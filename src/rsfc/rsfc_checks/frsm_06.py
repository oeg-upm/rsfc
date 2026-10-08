from rsfc.utils import constants
from rsfc.model import check as ch
from rsfc.utils.registry import test_registry

################################################### FRSM_06 ###################################################


@test_registry.register_test("RSFC-06-1", args=["somef_data"])
def test_authors(somef_data):
    unique_sources = set()

    if "author" in somef_data and isinstance(somef_data["author"], list):
        for item in somef_data["author"]:
            if "source" in item:
                sources = item["source"]
                sources_list = sources if isinstance(sources, list) else [sources]
                for s in sources_list:
                    if s and str(s).strip():
                        unique_sources.add(str(s).strip())

    if "citation" in somef_data and isinstance(somef_data["citation"], list):
        for item in somef_data["citation"]:
            if "result" in item and "author" in item["result"] and item["result"]["author"]:
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
        evidence = constants.EVIDENCE_AUTHORS + formatted_sources
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_AUTHORS
        suggest = constants.SUGGEST_NO_AUTHORS

    check = ch.Check(constants.INDICATORS_DICT['descriptive_metadata'], 'RSFC-06-1', "Authors are declared", constants.PROCESS_AUTHORS, output, evidence, suggest)

    return check.convert()


@test_registry.register_test("RSFC-06-2", args=["somef_data"])
def test_contributors(somef_data):
    unique_sources = set()

    if "contributor" in somef_data and isinstance(somef_data["contributor"], list):
        for item in somef_data["contributor"]:
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
        evidence = constants.EVIDENCE_CONTRIBUTORS + formatted_sources
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_CONTRIBUTORS
        suggest = constants.SUGGEST_NO_CONTRIBUTORS

    check = ch.Check(constants.INDICATORS_DICT['has_active_contributors'], 'RSFC-06-2', "Contributors are declared", constants.PROCESS_CONTRIBUTORS, output, evidence, suggest)

    return check.convert()


@test_registry.register_test("RSFC-06-3", args=["somef_data"])
def test_authors_orcids(somef_data):
    missing_orcid_sources = set()

    has_codemeta_authors = False
    has_cff_authors = False

    if "author" in somef_data and isinstance(somef_data["author"], list):
        for item in somef_data["author"]:
            if "result" in item:
                sources = item.get("source", [])
                sources_list = sources if isinstance(sources, list) else [sources]

                is_codemeta = any("codemeta" in str(s) for s in sources_list)

                if is_codemeta:
                    has_codemeta_authors = True
                    orcid_id = item["result"].get("identifier", "")

                    if not orcid_id or "https://orcid.org/" not in str(orcid_id):
                        for s in sources_list:
                            if "codemeta" in str(s):
                                missing_orcid_sources.add(str(s).strip())

    if "citation" in somef_data and isinstance(somef_data["citation"], list):
        for item in somef_data["citation"]:
            sources = item.get("source", [])
            sources_list = sources if isinstance(sources, list) else [sources]

            if not any("CITATION.cff" in str(s) for s in sources_list):
                continue

            authors = item.get("result", {}).get("author", [])
            if authors:
                has_cff_authors = True

                for author in authors:
                    orcid_url = author.get("url", "")
                    if not orcid_url or "orcid.org" not in str(orcid_url):
                        for s in sources_list:
                            if "CITATION.cff" in str(s):
                                missing_orcid_sources.add(str(s).strip())

    if (has_codemeta_authors or has_cff_authors) and not missing_orcid_sources:
        output = "true"
        evidence = constants.EVIDENCE_AUTHOR_ORCIDS
        suggest = "N/A"
    else:
        output = "false"
        suggest = constants.SUGGEST_NO_AUTHOR_ORCIDS

        if missing_orcid_sources:
            formatted_sources = "".join([f"\n\t- {src}" for src in sorted(missing_orcid_sources)])
            evidence = constants.EVIDENCE_NO_AUTHOR_ORCIDS + formatted_sources
        else:
            evidence = constants.EVIDENCE_NO_AUTHOR_ORCIDS + "\n\t- No author sources found to analyze"

    check = ch.Check(constants.INDICATORS_DICT['descriptive_metadata'], 'RSFC-06-3', "Authors have an ORCID", constants.PROCESS_AUTHOR_ORCIDS, output, evidence, suggest)

    return check.convert()

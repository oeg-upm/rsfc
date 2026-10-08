from rsfc.utils import constants
from rsfc.model import check as ch
from rsfc.utils.registry import test_registry

################################################### FRSM_12 ###################################################


@test_registry.register_test("RSFC-12-1", args=["somef_data"])
def test_reference_publication(somef_data):
    ref_pub_found = []
    article_citations_found = []

    if "citation" in somef_data:
        for item in somef_data["citation"]:
            if "source" in item and "result" in item:
                sources = item["source"]
                sources_list = sources if isinstance(sources, list) else [sources]

                is_ref_pub = any("codemeta" in str(s) for s in sources_list)

                result_data = item["result"]
                is_article = False
                if "format" in result_data and result_data["format"] == "bibtex":
                    is_article = True
                elif "type" in result_data and (
                    result_data["type"] == "ScholarlyArticle"
                    or result_data["type"] == "article"
                ):
                    is_article = True

                title = result_data.get("title", "Untitled Citation")

                if is_ref_pub:
                    ref_pub_found.append(title)
                if is_article:
                    article_citations_found.append(title)

    if article_citations_found and ref_pub_found:
        output = "true"
        suggest = "N/A"

        all_found = ref_pub_found + article_citations_found
        formatted_sources = "".join([f"\n\t- {title}" for title in all_found])
        evidence = (
            constants.EVIDENCE_REFERENCE_PUBLICATION_OR_CITATION_TO_ARTICLE
            + formatted_sources
        )

    elif article_citations_found:
        output = "true"
        suggest = "N/A"

        formatted_sources = "".join(
            [f"\n\t- {title}" for title in article_citations_found]
        )
        evidence = constants.EVIDENCE_ARTICLE_CITATION + formatted_sources

    elif ref_pub_found:
        output = "true"
        suggest = "N/A"

        formatted_sources = "".join([f"\n\t- {title}" for title in ref_pub_found])
        evidence = constants.EVIDENCE_REFERENCE_PUBLICATION + formatted_sources

    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_REFERENCE_PUBLICATION_OR_CITATION_TO_ARTICLE
        suggest = constants.SUGGEST_NO_REFPUB_OR_ARTICLE

    check = ch.Check(
        constants.INDICATORS_DICT["software_has_citation"],
        "RSFC-12-1",
        "There is an article citation or reference publication",
        constants.PROCESS_REFERENCE_PUBLICATION,
        output,
        evidence,
        suggest,
    )

    return check.convert()

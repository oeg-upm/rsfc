from rsfc.utils import constants
from rsfc.model import check as ch
from rsfc.utils.registry import test_registry

################################################### FRSM_04 ###################################################


@test_registry.register_test("RSFC-04-1", args=["somef_data", "gh_data"])
def test_metadata_exists(somef_data, gh_data):
    metadata_files = {
        'CITATION.cff': False,
        'codemeta.json': False,
        'package_file': False
    }

    if gh_data.cff is not None:
        metadata_files['CITATION.cff'] = True

    if gh_data.codemeta is not None:
        metadata_files['codemeta.json'] = True

    if 'has_package_file' in somef_data:
        metadata_files['package_file'] = True

    if any(metadata_files.values()):
        output = "true"
        suggest = "N/A"

        existing_metadata = [key for key, value in metadata_files.items() if value]
        existing_metadata_txt = ', '.join(existing_metadata)

        evidence = constants.EVIDENCE_METADATA_EXISTS.format(source=existing_metadata_txt)
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_METADATA_EXISTS
        suggest = constants.SUGGEST_NO_METADATA_FILES

    check = ch.Check(constants.INDICATORS_DICT['descriptive_metadata'], 'RSFC-04-1', "Metadata exists", constants.PROCESS_METADATA_EXISTS, output, evidence, suggest)

    return check.convert()


@test_registry.register_test("RSFC-04-2", args=["somef_data"])
def test_readme_exists(somef_data):
    if 'readme_url' in somef_data:
        output = "true"
        evidence = constants.EVIDENCE_DOCUMENTATION_README
        suggest = "N/A"
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_DOCUMENTATION_README
        suggest = constants.SUGGEST_NO_README

    check = ch.Check(constants.INDICATORS_DICT['software_has_documentation'], 'RSFC-04-2', "There is a README", constants.PROCESS_README, output, evidence, suggest)

    return check.convert()


@test_registry.register_test("RSFC-04-3", args=["somef_data"])
def test_title_description(somef_data):
    title_evidence_part = None
    desc_evidence_part = None

    if 'full_title' in somef_data and isinstance(somef_data['full_title'], list) and len(somef_data['full_title']) > 0:
        item = somef_data['full_title'][0]
        if "source" in item:
            sources = item["source"]
            sources_list = sources if isinstance(sources, list) else [sources]
            title_txt = ", ".join(sorted([str(s).strip() for s in sources_list if s and str(s).strip()]))
            title_evidence_part = f"title in {title_txt}"
        elif "technique" in item:
            tech = item["technique"]
            title_evidence_part = f"title (no source found, obtained via {tech})"
        else:
            title_evidence_part = "title (no source or technique found)"

    if 'description' in somef_data and isinstance(somef_data['description'], list) and len(somef_data['description']) > 0:
        item = somef_data['description'][0]
        if "source" in item:
            sources = item["source"]
            sources_list = sources if isinstance(sources, list) else [sources]
            desc_txt = ", ".join(sorted([str(s).strip() for s in sources_list if s and str(s).strip()]))
            desc_evidence_part = f"description in {desc_txt}"
        elif "technique" in item:
            tech = item["technique"]
            desc_evidence_part = f"description (no source found, obtained via {tech})"
        else:
            desc_evidence_part = "description (no source or technique found)"

    if title_evidence_part and desc_evidence_part:
        output = "true"
        suggest = "N/A"
        if "in " in title_evidence_part and "in " in desc_evidence_part:
            t_clean = title_evidence_part.replace("title in ", "")
            d_clean = desc_evidence_part.replace("description in ", "")
            evidence = constants.EVIDENCE_TITLE_AND_DESCRIPTION.format(title_sources=t_clean, desc_sources=d_clean)
        else:
            evidence = f"Found {title_evidence_part} and {desc_evidence_part}."

    elif title_evidence_part and not desc_evidence_part:
        output = "false"
        suggest = constants.SUGGEST_NO_DESCRIPTION
        evidence = f"Found {title_evidence_part}. However, no description was found."

    elif desc_evidence_part and not title_evidence_part:
        output = "false"
        suggest = constants.SUGGEST_NO_TITLE
        evidence = f"Found {desc_evidence_part}. However, no title was found."

    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_TITLE_AND_DESCRIPTION
        suggest = constants.SUGGEST_NO_TITLE_DESCRIPTION

    check = ch.Check(constants.INDICATORS_DICT['descriptive_metadata'], 'RSFC-04-3', "There are title and description", constants.PROCESS_TITLE_DESCRIPTION, output, evidence, suggest)

    return check.convert()


@test_registry.register_test("RSFC-04-4", args=["somef_data"])
def test_descriptive_metadata(somef_data):
    desc_sources = set()
    lang_sources = set()
    date_sources = set()
    keyword_sources = set()

    if 'description' in somef_data and isinstance(somef_data['description'], list):
        for item in somef_data['description']:
            if "source" in item:
                sources = item["source"]
                sources_list = sources if isinstance(sources, list) else [sources]
                for s in sources_list:
                    if s and str(s).strip():
                        desc_sources.add(str(s).strip())

    if 'programming_languages' in somef_data and isinstance(somef_data['programming_languages'], list):
        for item in somef_data['programming_languages']:
            if "source" in item:
                sources = item["source"]
                sources_list = sources if isinstance(sources, list) else [sources]
                for s in sources_list:
                    if s and str(s).strip():
                        lang_sources.add(str(s).strip())

    if 'date_created' in somef_data and isinstance(somef_data['date_created'], list):
        for item in somef_data['date_created']:
            if "source" in item:
                sources = item["source"]
                sources_list = sources if isinstance(sources, list) else [sources]
                for s in sources_list:
                    if s and str(s).strip():
                        date_sources.add(str(s).strip())

    if 'keywords' in somef_data and isinstance(somef_data['keywords'], list):
        for item in somef_data['keywords']:
            if "source" in item:
                sources = item["source"]
                sources_list = sources if isinstance(sources, list) else [sources]
                for s in sources_list:
                    if s and str(s).strip():
                        keyword_sources.add(str(s).strip())

    has_all_metadata = all([desc_sources, lang_sources, date_sources, keyword_sources])

    txt_desc = ", ".join(sorted(desc_sources)) if desc_sources else "None"
    txt_lang = ", ".join(sorted(lang_sources)) if lang_sources else "None"
    txt_date = ", ".join(sorted(date_sources)) if date_sources else "None"
    txt_key  = ", ".join(sorted(keyword_sources)) if keyword_sources else "None"

    if has_all_metadata:
        output = "true"
        suggest = "N/A"
        evidence = constants.EVIDENCE_DESCRIPTIVE_METADATA.format(desc_sources=txt_desc, lang_sources=txt_lang, date_sources=txt_date, keyword_sources=txt_key)
    else:
        output = "false"
        suggest = constants.SUGGEST_NO_DESCRIPTIVE_METADATA
        evidence = constants.EVIDENCE_NO_DESCRIPTIVE_METADATA.format(desc_sources=txt_desc, lang_sources=txt_lang, date_sources=txt_date, keyword_sources=txt_key)

    check = ch.Check(constants.INDICATORS_DICT['descriptive_metadata'], 'RSFC-04-4', "Software has descriptive metadata", constants.PROCESS_DESCRIPTIVE_METADATA, output, evidence, suggest)

    return check.convert()


@test_registry.register_test("RSFC-04-5", args=["gh_data"])
def test_codemeta_exists(gh_data):
    if gh_data.codemeta != None:
        output = "true"
        evidence = constants.EVIDENCE_METADATA_CODEMETA
        suggest = "N/A"
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_METADATA_CODEMETA
        suggest = constants.SUGGEST_NO_CODEMETA

    check = ch.Check(constants.INDICATORS_DICT['descriptive_metadata'], 'RSFC-04-5', "There is a codemeta file", constants.PROCESS_CODEMETA, output, evidence, suggest)

    return check.convert()

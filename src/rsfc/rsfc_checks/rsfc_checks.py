from rsfc.utils import constants
from rsfc.model import check as ch
import regex as re
import requests
from rsfc.utils import rsfc_helpers


################################################### FRSM_01 ###################################################

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
                        output = "error"
                        evidence = "Something went wrong when trying to resolve the identifier"
                        suggest = None

                else:
                    output = "false"
                    evidence = constants.EVIDENCE_ID_NOT_URL.format(id=identifier)
                    suggest = constants.SUGGEST_IDENTIFIER_NOT_HTTP

    check = ch.Check(constants.INDICATORS_DICT['persistent_and_unique_identifier'], 'RSFC-01-1', "There is an identifier and resolves", constants.PROCESS_IDENTIFIER, output, evidence, suggest)

    return check.convert()


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



################################################### FRSM_03 ###################################################


def test_version_number_in_metadata(somef_data):

    if 'version' in somef_data:
        output = "true"
        suggest = "N/A"

        sources = set()

        for item in somef_data["version"]:
            source = item.get("source", [])

            if isinstance(source, list):
                sources.update(source)
            else:
                sources.add(source)

        valid_sources = ''.join(f'\n\t- {source}' for source in sorted(sources))
        evidence = constants.EVIDENCE_VERSION_IN_METADATA + valid_sources

    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_VERSION_IN_METADATA
        suggest = constants.SUGGEST_NO_VERSION_IN_METADATA

    check = ch.Check(constants.INDICATORS_DICT['descriptive_metadata'], 'RSFC-03-6', "Version number in metadata", constants.PROCESS_VERSION_IN_METADATA, output, evidence, suggest)

    return check.convert()


def test_has_releases(somef_data):
    if 'releases' not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_RELEASES
        suggest = constants.SUGGEST_NO_RELEASES
    else:
        output = "true"
        evidence = constants.EVIDENCE_RELEASES
        suggest = "N/A"
        for item in somef_data['releases']:
            if 'type' in item['result']:
                if item['result']['type'] == 'Release':
                    evidence += f'\n\t- {item["result"]["html_url"]}'
                        
    check = ch.Check(constants.INDICATORS_DICT['has_releases'], 'RSFC-03-1', "Software has releases", constants.PROCESS_RELEASES, output, evidence, suggest)

    return check.convert()
    
    
def test_release_id_and_version(somef_data):
    if 'releases' not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_RELEASES
        suggest = constants.SUGGEST_NO_RELEASES
    else:
        output = "true"
        evidence = constants.EVIDENCE_RELEASE_ID_AND_VERSION
        suggest = "N/A"
        
        bad_releases = ""
        
        results = somef_data['releases']
        for item in results:
            if not (item['result']['url'] and item['result']['tag']):
                if output != "false":
                    output = "false"
                    suggest = constants.SUGGEST_NO_RELEASE_ID_AND_VERSION
                bad_releases += f"\t\n- {item['result']['html_url']}"
        
        if output == "false":
            evidence = constants.EVIDENCE_NO_RELEASE_ID_AND_VERSION + bad_releases
                
    check = ch.Check(constants.INDICATORS_DICT['has_releases'], 'RSFC-03-2', "Releases have an id and version number", constants.PROCESS_RELEASE_ID_VERSION, output, evidence, suggest)
    
    return check.convert()


def test_semantic_versioning_standard(somef_data):
    if 'releases' not in somef_data or not isinstance(somef_data['releases'], list) or len(somef_data['releases']) == 0:
        output = "false"
        evidence = constants.EVIDENCE_NO_RELEASES
        suggest = constants.SUGGEST_NO_RELEASES
    else:
        compiled_patterns = [re.compile(pattern) for pattern in constants.VERSIONING_REGEX_LIST]
        bad_versions_list = []
        total_valid_tags = 0
        
        results = somef_data['releases']
        for item in results:
            if 'result' in item and 'tag' in item['result']:
                tag_value = item['result']['tag']
                if tag_value:
                    total_valid_tags += 1
                    if not any(pattern.match(str(tag_value)) for pattern in compiled_patterns):
                        bad_versions_list.append(str(tag_value))
        
        if total_valid_tags == 0:
            output = "false"
            evidence = constants.EVIDENCE_NO_RELEASES
            suggest = constants.SUGGEST_NO_RELEASES
        else:
            successful_versions = total_valid_tags - len(bad_versions_list)
            success_rate = successful_versions / total_valid_tags
            
            bad_versions_txt = "".join([f"\n\t- {tag}" for tag in bad_versions_list])
            
            if success_rate >= 0.80:
                output = "true"
                suggest = "N/A"
                evidence = constants.EVIDENCE_VERSIONING_STANDARD
                
                if bad_versions_list:
                    evidence += f"\nNote: Some versions did not follow the convention but passed the 80% threshold:{bad_versions_txt}"
            else:
                output = "false"
                suggest = constants.SUGGEST_NO_VERSIONING_STANDARD
                evidence = constants.EVIDENCE_NO_VERSIONING_STANDARD + bad_versions_txt
                
    check = ch.Check(constants.INDICATORS_DICT['versioning_standards_use'], 'RSFC-03-3', "Release versions follow a community established convention", constants.PROCESS_SEMANTIC_VERSIONING, output, evidence, suggest)
    
    return check.convert()
        
    
def test_version_scheme(somef_data):
    if 'releases' not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_RELEASES
        suggest = constants.SUGGEST_NO_RELEASES
    else:
        output = "true"
        evidence = constants.EVIDENCE_IDENTIFIER_SCHEME_COMPLIANT
        suggest = "N/A"
        
        scheme = ''
        bad_urls = ""
        
        results = somef_data['releases']
        for item in results:
            if 'result' in item and 'url' in item['result'] and item['result']['url']:
                url = item['result']['url']
                
                if not scheme:
                    scheme = rsfc_helpers.build_url_pattern(url)
                
                if scheme and not scheme.match(url):
                    if output != "false":
                        output = "false"
                        suggest = constants.SUGGEST_NO_IDENTIFIER_SCHEME_COMPLIANT
                    
                    bad_urls += f"\n\t- {url}"
        
        if output == "false":
            evidence = constants.EVIDENCE_NO_IDENTIFIER_SCHEME_COMPLIANT + bad_urls
        
    check = ch.Check(constants.INDICATORS_DICT['has_releases'], 'RSFC-03-4', "Release identifiers follow the same scheme", constants.PROCESS_VERSION_SCHEME, output, evidence, suggest)
    
    return check.convert()



def test_latest_release_consistency(somef_data):
    latest_release = None
    version = None
    
    if 'releases' in somef_data:
        latest_release = rsfc_helpers.get_latest_release(somef_data)
        
    if 'version' in somef_data:
        version_data = somef_data['version'][0]['result']
        version = version_data.get('tag') or version_data.get('value')
        
    norm_version = str(version).strip().lstrip('vV')
    norm_latest = str(latest_release).strip().lstrip('vV')
    
    if version == None or latest_release == None:
        output = "error"
        evidence = constants.EVIDENCE_NOT_ENOUGH_RELEASE_INFO
        suggest = None
    elif norm_version == norm_latest:
        output = "true"
        evidence = constants.EVIDENCE_RELEASE_CONSISTENCY
        suggest = "N/A"
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_RELEASE_CONSISTENCY
        suggest = constants.SUGGEST_NO_RELEASE_CONSISTENCY
        
        
    check = ch.Check(constants.INDICATORS_DICT['has_releases'], 'RSFC-03-5', "Last release consistency", constants.PROCESS_RELEASE_CONSISTENCY, output, evidence, suggest)
    
    return check.convert()

################################################### FRSM_04 ###################################################

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

################################################### FRSM_05 ###################################################

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

################################################### FRSM_06 ###################################################

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
        
    check = ch.Check(constants.INDICATORS_DICT['descriptive_metadata'], 'RSFC-06-2', "Contributors are declared", constants.PROCESS_CONTRIBUTORS, output, evidence, suggest)
    
    return check.convert()


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


'''def test_author_roles(codemeta_data):
    
    if codemeta_data != None:
        if codemeta_data["author"] != None:
            author_roles = rsfc_helpers.subtest_author_roles(codemeta_data["author"])
            
            if all(value is not None for value in author_roles.values()):
                output = "true"
                evidence = constants.EVIDENCE_AUTHOR_ROLES
                suggest = "N/A"
            else:
                output = "false"
                evidence = constants.EVIDENCE_NO_ALL_AUTHOR_ROLES
                suggest = constants.SUGGEST_NO_ALL_AUTHOR_ROLES
        else:
            output = "false"
            evidence = constants.EVIDENCE_NO_AUTHORS_IN_CODEMETA
            suggest = constants.SUGGEST_NO_AUTHORS_IN_CODEMETA
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_CODEMETA_FOUND
        suggest = constants.SUGGEST_NO_CODEMETA
        
    check = ch.Check(constants.INDICATORS_DICT['descriptive_metadata'], 'RSFC-06-4', "Authors have roles", constants.PROCESS_AUTHOR_ROLES, output, evidence, suggest)
    
    return check.convert()'''

################################################### FRSM_07 ###################################################

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

################################################### FRSM_08 ###################################################

def test_metadata_record_in_zenodo_or_software_heritage(somef_data):
    zenodo_identifiers = []
    swh_identifiers = []
    
    if "identifier" in somef_data:
        for item in somef_data['identifier']:
            if 'result' in item and 'value' in item['result'] and item['result']['value']:
                val = item['result']['value']
                
                if 'zenodo' in val:
                    zenodo_identifiers.append(val)
                elif 'softwareheritage' in val:
                    swh_identifiers.append(val)

    if zenodo_identifiers and swh_identifiers:
        output = "true"
        suggest = "N/A"
        
        all_ids = zenodo_identifiers + swh_identifiers
        formatted_ids = "".join([f"\n\t- {id_val}" for id_val in all_ids])
        evidence = constants.EVIDENCE_ZENODO_DOI_AND_SOFTWARE_HERITAGE + formatted_ids
        
    elif swh_identifiers:
        output = "true"
        suggest = "N/A"
        
        formatted_ids = "".join([f"\n\t- {id_val}" for id_val in swh_identifiers])
        evidence = constants.EVIDENCE_SOFTWARE_HERITAGE_BADGE + formatted_ids
        
    elif zenodo_identifiers:
        output = "true"
        suggest = "N/A"
        
        formatted_ids = "".join([f"\n\t- {id_val}" for id_val in zenodo_identifiers])
        evidence = constants.EVIDENCE_ZENODO_DOI + formatted_ids
        
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_ZENODO_DOI_OR_SOFTWARE_HERITAGE
        suggest = constants.SUGGEST_ARCHIVE_SOFTWARE
        
    check = ch.Check(constants.INDICATORS_DICT['archived_in_software_heritage'], 'RSFC-08-1', "Metadata record in Software Heritage or Zenodo", constants.PROCESS_ZENODO_SOFTWARE_HERITAGE, output, evidence, suggest)
    
    return check.convert()

################################################### FRSM_09 ###################################################

def test_is_github_repository(repo_url):

    if 'github.com' in repo_url or 'gitlab.com' in repo_url:
        response = requests.head(repo_url, allow_redirects=True, timeout=5)
        if response.status_code == 200:
            output = "true"
            evidence = constants.EVIDENCE_IS_IN_GITHUB_OR_GITLAB
            suggest = "N/A"
        elif response.status_code == 404:
            output = "false"
            evidence = constants.EVIDENCE_NO_RESOLVE_GITHUB_OR_GITLAB_URL
            suggest = "N/A"
        else:
            output = "error"
            evidence = 'Connection error'
            suggest = "N/A"
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_GITHUB_OR_GITLAB_URL
        suggest = "N/A"
    
    check = ch.Check(constants.INDICATORS_DICT['version_control_use'], 'RSFC-09-1', "Repository is from Github/Gitlab", constants.PROCESS_IS_GITHUB_OR_GITLAB_REPOSITORY, output, evidence, suggest)
    
    return check.convert()

################################################### FRSM_12 ###################################################

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
                if 'format' in result_data and result_data['format'] == 'bibtex':
                    is_article = True
                elif 'type' in result_data and (result_data['type'] == 'ScholarlyArticle' or result_data['type'] == 'article'):
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
        evidence = constants.EVIDENCE_REFERENCE_PUBLICATION_OR_CITATION_TO_ARTICLE + formatted_sources
        
    elif article_citations_found:
        output = "true"
        suggest = "N/A"
        
        formatted_sources = "".join([f"\n\t- {title}" for title in article_citations_found])
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
        
    check = ch.Check(constants.INDICATORS_DICT['software_has_citation'], 'RSFC-12-1', "There is an article citation or reference publication", constants.PROCESS_REFERENCE_PUBLICATION, output, evidence, suggest)
    
    return check.convert()

################################################### FRSM_13 ###################################################

def test_dependencies_declared(somef_data):
    if 'requirements' not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_DEPENDENCIES
        suggest = constants.SUGGEST_NO_DEPENDENCIES
    else:
        output = "true"
        evidence = constants.EVIDENCE_DEPENDENCIES
        suggest = "N/A"
        
        for item in somef_data['requirements']:
            sources = item.get("source", [])
            sources_list = sources if isinstance(sources, list) else [sources]
            
            sources_str = ", ".join(sources_list)
            
            if sources_str not in evidence:
                evidence += f'\n\t- {sources_str}'

    check = ch.Check(constants.INDICATORS_DICT['requirements_specified'], 'RSFC-13-1', "Dependencies are declared", constants.PROCESS_REQUIREMENTS, output, evidence, suggest)
    
    return check.convert()


def test_installation_instructions(somef_data):
    if 'installation' in somef_data and somef_data['installation']:
        output = "false"
        evidence = constants.EVIDENCE_NO_INSTALLATION
        suggest = constants.SUGGEST_NO_INSTALL_INSTRUCTIONS
        unique_sources = set()
        
        for item in somef_data['installation']:
            if "source" in item:
                sources = item["source"]
                
                if isinstance(sources, list):
                    for s in sources:
                        if s and str(s).strip():
                            unique_sources.add(str(s).strip())
                elif isinstance(sources, str) and sources.strip():
                    unique_sources.add(sources.strip())
                    
        if unique_sources:
            output = "true"
            suggest = "N/A"
            formatted_sources = "".join([f"\n\t- {src}" for src in sorted(unique_sources)])
            evidence = constants.EVIDENCE_INSTALLATION + formatted_sources
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_INSTALLATION
        suggest = constants.SUGGEST_NO_INSTALL_INSTRUCTIONS
        
    check = ch.Check(constants.INDICATORS_DICT['software_has_documentation'], 'RSFC-13-2', "There are installation instructions", constants.PROCESS_INSTALLATION, output, evidence, suggest)
    
    return check.convert()


def test_dependencies_have_version(somef_data):
    if 'requirements' not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_DEPENDENCIES
        suggest = constants.SUGGEST_NO_DEPENDENCIES
    else:
        output = "true"
        evidence = constants.EVIDENCE_DEPENDENCIES_VERSION
        suggest = "N/A"
        
        bad_dependencies = ""
        
        for item in somef_data['requirements']:
            if "source" in item and "result" in item:
                sources = item['source']
                sources_list = sources if isinstance(sources, list) else [sources]
                
                if any('README' in str(s) for s in sources_list):
                    continue
                
                version = item["result"].get("version")
                
                if not version or (isinstance(version, str) and not version.strip()):
                    if output != "false":
                        output = "false"
                        suggest = constants.SUGGEST_NO_DEPENDENCIES_VERSION
                    
                    dep_name = item["result"].get("name", "Unknown dependency")
                    bad_dependencies += f"\n\t- {dep_name}"
        
        if output == "false":
            evidence = constants.EVIDENCE_NO_DEPENDENCIES_VERSION + bad_dependencies
            
    check = ch.Check(constants.INDICATORS_DICT['requirements_specified'], 'RSFC-13-3', "Dependencies have version numbers", constants.PROCESS_DEPENDENCIES_VERSION, output, evidence, suggest)
    
    return check.convert()


def test_dependencies_in_machine_readable_file(somef_data):
    if 'requirements' not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_DEPENDENCIES
        suggest = constants.SUGGEST_NO_DEPENDENCIES
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_DEPENDENCIES_MACHINE_READABLE_FILE
        suggest = constants.SUGGEST_NO_MACHINE_READABLE_DEPENDENCIES
        
        valid_sources = ""
        
        for item in somef_data['requirements']:
            if "source" in item:
                sources = item['source']

                if isinstance(sources, list):
                    for s in sources:
                        if 'README' not in s:
                            if output != "true":
                                output = "true"
                                suggest = "N/A"
                            valid_sources += f"\n\t- {s}"

                elif isinstance(sources, str) and sources:
                    if 'README' not in sources:
                        if output != "true":
                            output = "true"
                            suggest = "N/A"
                        valid_sources += f"\n\t- {sources}"
                        
        if output == "true":
            evidence = constants.EVIDENCE_DEPENDENCIES_MACHINE_READABLE_FILE + valid_sources
            
    check = ch.Check(constants.INDICATORS_DICT['requirements_specified'], 'RSFC-13-4', "There is a dependencies machine-readable file", constants.PROCESS_DEPENDENCIES_MACHINE_READABLE_FILE, output, evidence, suggest)
    
    return check.convert()


################################################### FRSM_14 ###################################################

def test_presence_of_tests(gh):
    test_evidences = gh.tests

    if test_evidences:
        rx = re.compile(r'tests?', re.IGNORECASE)
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
        output = "error"
        evidence = None
        suggest = constants.SUGGEST_NO_TESTS
            
    check = ch.Check(constants.INDICATORS_DICT['software_has_tests'], 'RSFC-14-1', "Presence of tests in repository", constants.PROCESS_TESTS, output, evidence, suggest)
    
    return check.convert()


def test_github_action_tests(somef_data):
    sources = ''
    
    if 'continuous_integration' not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_WORKFLOWS
        suggest = constants.SUGGEST_NO_WORKFLOWS
        
    else:
        for item in somef_data['continuous_integration']:
            if item['result']['value'] and ('.github/workflows' in item['result']['value'] or '.gitlab-ci.yml' in item['result']['value']):
                if any(keyword in item['result']['value'] for keyword in ["test", "validate", "check"]):
                    sources += f'\n\t- {item["result"]["value"]}'
                    
    if sources:
        output = "true"
        evidence = constants.EVIDENCE_AUTOMATED_TESTS + sources
        suggest = "N/A"
        
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_AUTOMATED_TESTS
        suggest = constants.SUGGEST_NO_TEST_ACTIONS
        
        
    check = ch.Check(constants.INDICATORS_DICT['repository_workflows'], 'RSFC-14-2', "There are actions to automate tests", constants.PROCESS_AUTOMATED_TESTS, output, evidence, suggest)
    
    return check.convert()

'''def test_has_no_known_bugs(gh_data):
    if len(gh_data.bug_issues) == 0:
        output = "true"
        evidence = constants.EVIDENCE_NO_ISSUES_BUG
        suggest = "N/A"
    else:
        output = "false"
        evidence = constants.EVIDENCE_ISSUES_BUGS
        suggest = constants.SUGGEST_ISSUES_BUGS
        
    check = ch.Check(constants.INDICATORS_DICT['software_has_no_known_bugs'], 'RSFC-14-3', "Software has no issues tagged as bugs", constants.PROCESS_ISSUES_BUGS, output, evidence, suggest)
    
    return check.convert()'''

################################################### FRSM_15 ###################################################

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

################################################### FRSM_16 ###################################################

def test_license_info_in_metadata_files(somef_data):
    license_info = {
        'codemeta': None,
        'CITATION.cff': None,
        'package': None
    }
    
    if 'license' in somef_data:
        for item in somef_data['license']:
            sources = item.get("source", [])
            sources_list = sources if isinstance(sources, list) else [sources]
            for s in sources_list:
                if 'pyproject.toml' in s or 'setup.py' in s or 'node.json' in s or 'pom.xml' in s or 'package.json' in s:
                    license_info['package'] = item["result"]["value"]
                if "codemeta" in s:
                    license_info["codemeta"] = item["result"]["value"]
                if "CITATION.cff" in s:
                    license_info["CITATION.cff"] = item["result"]["value"]
                
    if all(license_info.values()):
        output = "true"
        suggest = "N/A"
        
        existing_list = [f"{key} ({value})" for key, value in license_info.items()]
        existing_txt = ', '.join(existing_list)
        
        evidence = constants.EVIDENCE_LICENSE_INFO_ALL.format(existing=existing_txt)

    elif any(license_info.values()):
        output = "true"
        suggest = "N/A"
        
        existing_list = [f"{key} ({value})" for key, value in license_info.items() if value]
        existing_txt = ', '.join(existing_list)
        
        missing_list = [key for key, value in license_info.items() if not value]
        missing_txt = ', '.join(missing_list)
        
        evidence = constants.EVIDENCE_LICENSE_INFO_IN_METADATA.format(existing=existing_txt, missing=missing_txt)

    else:
        output = "false"
        suggest = constants.SUGGEST_NO_LICENSE_INFO_METADATA
        
        missing_list = [key for key, value in license_info.items()]
        missing_txt = ', '.join(missing_list)
        
        evidence = constants.EVIDENCE_NO_LICENSE_INFO_IN_METADATA + ": " + missing_txt
        
    check = ch.Check(constants.INDICATORS_DICT['software_has_license'], 'RSFC-16-1', "License referenced in metadata files", constants.PROCESS_LICENSE_INFO_IN_METADATA_FILES, output, evidence, suggest)
    
    return check.convert()

################################################### FRSM_17 ###################################################

'''def test_repo_enabled_and_commits(somef_data, gh):
    
    if 'repository_status' in somef_data and somef_data['repository_status'][0]['result']['value']:
        if '#active' in somef_data['repository_status'][0]['result']['value']:
            repo = True
        else:
            repo = False
    else:
        repo = False
        
    commits = gh.commits

    if repo:
        if commits:
            output = "true"
            evidence = constants.EVIDENCE_REPO_ENABLED_AND_HAS_COMMITS
            suggest = "N/A"
        else:
            output = "false"
            evidence = constants.EVIDENCE_NO_COMMITS
            suggest = constants.SUGGEST_NO_COMMITS
            
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_REPO_STATUS
        suggest = constants.SUGGEST_NO_ACTIVE_REPO
        
        
    check = ch.Check(constants.INDICATORS_DICT['project_is_active'], 'RSFC-17-1', "Repository is active", constants.PROCESS_REPO_ENABLED_AND_COMMITS, output, evidence, suggest)
    
    return check.convert()'''


def test_commit_history(gh):

    commits = gh.commits
    
    if commits[1] != []:
        output = "true"
        evidence = constants.EVIDENCE_COMMITS + f"\n\t- {commits[0]}"
        suggest = "N/A"
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_COMMITS
        suggest = constants.SUGGEST_NO_COMMITS
        
    check = ch.Check(constants.INDICATORS_DICT['version_control_use'], 'RSFC-17-2', "Commit history", constants.PROCESS_COMMITS_HISTORY, output, evidence, suggest)
    
    return check.convert()

def test_commits_linked_issues(gh):
    commits = gh.commits
    issues = gh.issues
    commits_list = commits[1]

    if commits_list == [] or issues == []:
        output = "false"
        evidence = constants.EVIDENCE_NOT_ENOUGH_ISSUES_COMMITS_INFO
        suggest = constants.SUGGEST_NO_COMMITS_OR_ISSUES
    else:
        linked_pairs = rsfc_helpers.cross_check_any_issue(issues, commits_list)
        
        if linked_pairs:
            output = "true"
            suggest = "N/A"
            
            formatted_pairs = "".join([f"\n\t- {pair}" for pair in linked_pairs])
            evidence = constants.EVIDENCE_COMMITS_LINKED_TO_ISSUES + formatted_pairs
        else:
            output = "false"
            evidence = constants.EVIDENCE_NO_COMMITS_LINKED_TO_ISSUES
            suggest = constants.SUGGEST_NO_ISSUES_LINK_COMMITS
            

    check = ch.Check(constants.INDICATORS_DICT['version_control_use'], 'RSFC-17-3', "Commits are linked to issues", constants.PROCESS_COMMITS_LINKED_TO_ISSUES, output, evidence, suggest)
    
    return check.convert()


################################################### MISC ###################################################


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


def test_has_issue_tracker(somef_data):
    
    if "issue_tracker" not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_ISSUE_TRACKER
        suggest = constants.SUGGEST_NO_ISSUE_TRACKER
    else:
        for item in somef_data["issue_tracker"]:
            sources = ""
            if "source" in item:
                sources += f"\n\t- {item['source']}"
                
        if sources:
            evidence = constants.EVIDENCE_ISSUE_TRACKER_SOURCE + sources
        else:
            evidence = constants.EVIDENCE_ISSUE_TRACKER_NO_SOURCE
            
        output = "true"
        suggest = "N/A"
        
    check = ch.Check(constants.INDICATORS_DICT['support_issue_tracking'], 'RSFC-20-1', "Repository has an issue tracker", constants.PROCESS_ISSUE_TRACKER, output, evidence, suggest)
    
    return check.convert()


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
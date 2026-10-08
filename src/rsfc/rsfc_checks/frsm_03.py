from rsfc.utils import constants
from rsfc.model import check as ch
import regex as re
from rsfc.utils import rsfc_helpers
from rsfc.utils.registry import test_registry

################################################### FRSM_03 ###################################################


@test_registry.register_test("RSFC-03-6", args=["somef_data"])
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


@test_registry.register_test("RSFC-03-1", args=["somef_data"])
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


@test_registry.register_test("RSFC-03-2", args=["somef_data"])
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
                bad_releases += f"\t\n- {item["result"]["html_url"]}"

        if output == "false":
            evidence = constants.EVIDENCE_NO_RELEASE_ID_AND_VERSION + bad_releases

    check = ch.Check(constants.INDICATORS_DICT['has_releases'], 'RSFC-03-2', "Releases have an id and version number", constants.PROCESS_RELEASE_ID_VERSION, output, evidence, suggest)

    return check.convert()


@test_registry.register_test("RSFC-03-3", args=["somef_data"])
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


@test_registry.register_test("RSFC-03-4", args=["somef_data"])
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


@test_registry.register_test("RSFC-03-5", args=["somef_data"])
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
        output = "indeterminate"
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

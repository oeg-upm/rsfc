from rsfc.utils import constants
from rsfc.model import check as ch
from rsfc.utils.registry import test_registry

################################################### FRSM_16 ###################################################


@test_registry.register_test("RSFC-16-1", args=["somef_data"])
def test_license_info_in_metadata_files(somef_data):
    license_info = {"codemeta": None, "CITATION.cff": None, "package": None}

    if "license" in somef_data:
        for item in somef_data["license"]:
            sources = item.get("source", [])
            sources_list = sources if isinstance(sources, list) else [sources]
            for s in sources_list:
                if (
                    "pyproject.toml" in s
                    or "setup.py" in s
                    or "node.json" in s
                    or "pom.xml" in s
                    or "package.json" in s
                ):
                    license_info["package"] = item["result"]["value"]
                if "codemeta" in s:
                    license_info["codemeta"] = item["result"]["value"]
                if "CITATION.cff" in s:
                    license_info["CITATION.cff"] = item["result"]["value"]

    if all(license_info.values()):
        output = "true"
        suggest = "N/A"

        existing_list = [f"{key} ({value})" for key, value in license_info.items()]
        existing_txt = ", ".join(existing_list)

        evidence = constants.EVIDENCE_LICENSE_INFO_ALL.format(existing=existing_txt)

    elif any(license_info.values()):
        output = "true"
        suggest = "N/A"

        existing_list = [
            f"{key} ({value})" for key, value in license_info.items() if value
        ]
        existing_txt = ", ".join(existing_list)

        missing_list = [key for key, value in license_info.items() if not value]
        missing_txt = ", ".join(missing_list)

        evidence = constants.EVIDENCE_LICENSE_INFO_IN_METADATA.format(
            existing=existing_txt, missing=missing_txt
        )

    else:
        output = "false"
        suggest = constants.SUGGEST_NO_LICENSE_INFO_METADATA

        missing_list = [key for key, value in license_info.items()]
        missing_txt = ", ".join(missing_list)

        evidence = constants.EVIDENCE_NO_LICENSE_INFO_IN_METADATA + ": " + missing_txt

    check = ch.Check(
        constants.INDICATORS_DICT["software_has_license"],
        "RSFC-16-1",
        "License referenced in metadata files",
        constants.PROCESS_LICENSE_INFO_IN_METADATA_FILES,
        output,
        evidence,
        suggest,
    )

    return check.convert()

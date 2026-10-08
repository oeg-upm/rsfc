from rsfc.utils import constants
from rsfc.model import check as ch
from rsfc.utils.registry import test_registry

################################################### FRSM_13 ###################################################


@test_registry.register_test("RSFC-13-1", args=["somef_data"])
def test_dependencies_declared(somef_data):
    if "requirements" not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_DEPENDENCIES
        suggest = constants.SUGGEST_NO_DEPENDENCIES
    else:
        output = "true"
        evidence = constants.EVIDENCE_DEPENDENCIES
        suggest = "N/A"

        for item in somef_data["requirements"]:
            sources = item.get("source", [])
            sources_list = sources if isinstance(sources, list) else [sources]

            sources_str = ", ".join(sources_list)

            if sources_str not in evidence:
                evidence += f"\n\t- {sources_str}"

    check = ch.Check(
        constants.INDICATORS_DICT["requirements_specified"],
        "RSFC-13-1",
        "Dependencies are declared",
        constants.PROCESS_REQUIREMENTS,
        output,
        evidence,
        suggest,
    )

    return check.convert()


@test_registry.register_test("RSFC-13-2", args=["somef_data"])
def test_installation_instructions(somef_data):
    if "installation" in somef_data and somef_data["installation"]:
        output = "false"
        evidence = constants.EVIDENCE_NO_INSTALLATION
        suggest = constants.SUGGEST_NO_INSTALL_INSTRUCTIONS
        unique_sources = set()

        for item in somef_data["installation"]:
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
            formatted_sources = "".join(
                [f"\n\t- {src}" for src in sorted(unique_sources)]
            )
            evidence = constants.EVIDENCE_INSTALLATION + formatted_sources
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_INSTALLATION
        suggest = constants.SUGGEST_NO_INSTALL_INSTRUCTIONS

    check = ch.Check(
        constants.INDICATORS_DICT["software_has_documentation"],
        "RSFC-13-2",
        "There are installation instructions",
        constants.PROCESS_INSTALLATION,
        output,
        evidence,
        suggest,
    )

    return check.convert()


@test_registry.register_test("RSFC-13-3", args=["somef_data"])
def test_dependencies_have_version(somef_data):
    if "requirements" not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_DEPENDENCIES
        suggest = constants.SUGGEST_NO_DEPENDENCIES
    else:
        output = "true"
        evidence = constants.EVIDENCE_DEPENDENCIES_VERSION
        suggest = "N/A"

        bad_dependencies = ""

        for item in somef_data["requirements"]:
            if "source" in item and "result" in item:
                sources = item["source"]
                sources_list = sources if isinstance(sources, list) else [sources]

                if any("README" in str(s) for s in sources_list):
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

    check = ch.Check(
        constants.INDICATORS_DICT["requirements_specified"],
        "RSFC-13-3",
        "Dependencies have version numbers",
        constants.PROCESS_DEPENDENCIES_VERSION,
        output,
        evidence,
        suggest,
    )

    return check.convert()


@test_registry.register_test("RSFC-13-4", args=["somef_data"])
def test_dependencies_in_machine_readable_file(somef_data):
    if "requirements" not in somef_data:
        output = "false"
        evidence = constants.EVIDENCE_NO_DEPENDENCIES
        suggest = constants.SUGGEST_NO_DEPENDENCIES
    else:
        output = "false"
        evidence = constants.EVIDENCE_NO_DEPENDENCIES_MACHINE_READABLE_FILE
        suggest = constants.SUGGEST_NO_MACHINE_READABLE_DEPENDENCIES

        valid_sources = ""

        for item in somef_data["requirements"]:
            if "source" in item:
                sources = item["source"]

                if isinstance(sources, list):
                    for s in sources:
                        if "README" not in s:
                            if output != "true":
                                output = "true"
                                suggest = "N/A"
                            valid_sources += f"\n\t- {s}"

                elif isinstance(sources, str) and sources:
                    if "README" not in sources:
                        if output != "true":
                            output = "true"
                            suggest = "N/A"
                        valid_sources += f"\n\t- {sources}"

        if output == "true":
            evidence = (
                constants.EVIDENCE_DEPENDENCIES_MACHINE_READABLE_FILE + valid_sources
            )

    check = ch.Check(
        constants.INDICATORS_DICT["requirements_specified"],
        "RSFC-13-4",
        "There is a dependencies machine-readable file",
        constants.PROCESS_DEPENDENCIES_MACHINE_READABLE_FILE,
        output,
        evidence,
        suggest,
    )

    return check.convert()

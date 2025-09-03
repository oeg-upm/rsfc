from rsfc.rsfc_tests import rsfc_tests as rt

class Indicator:
    
    def __init__(self, sw, somef, cd, cf):
        
        self.indicator_functions = {
            "persistent_and_unique_identifier": [
                (rt.test_id_presence_and_resolves, [somef.somef_data]),
                (rt.test_id_associated_with_software, [somef.somef_data, cd.codemeta_data, cf.cff_data]),
                (rt.test_id_common_schema, [somef.somef_data]),
                (rt.test_identifier_in_readme_citation, [somef.somef_data, cf.cff_data]),
                (rt.test_identifier_resolves_to_software, [somef.somef_data, cd.codemeta_data, cf.cff_data, sw])
            ],
            "requirements_specified": [
                (rt.test_dependencies_declared, [somef.somef_data]),
                (rt.test_dependencies_in_machine_readable_file, [somef.somef_data]),
                (rt.test_dependencies_have_version, [somef.somef_data])
            ],
            "has_releases": [
                (rt.test_has_releases, [somef.somef_data]),
                (rt.test_release_id_and_version, [somef.somef_data]),
                (rt.test_latest_release_consistency, [somef.somef_data])
            ],
            "versioning_standards_use": [
                (rt.test_semantic_versioning_standard, [somef.somef_data]),
                (rt.test_version_scheme, [somef.somef_data])
            ],
            "software_tests": [
                (rt.test_presence_of_tests, [sw])
            ],
            "repository_workflows": [
                (rt.test_github_action_tests, [somef.somef_data]),
                (rt.test_repository_workflows, [somef.somef_data])
            ],
            "version_control_use": [
                (rt.test_is_github_repository, [sw.url]),
                (rt.test_repo_enabled_and_commits, [somef.somef_data, sw]),
                (rt.test_repo_status, [somef.somef_data]),
                (rt.test_commit_history, [sw]),
                (rt.test_commits_linked_issues, [sw])
            ],
            "software_has_license": [
                (rt.test_has_license, [somef.somef_data]),
                (rt.test_license_spdx_compliant, [somef.somef_data]),
                (rt.test_license_info_in_metadata_files, [somef.somef_data, cd.codemeta_data, cf.cff_data]),
                (rt.test_license_information_provided, [somef.somef_data])
            ],
            "descriptive_metadata": [
                (rt.test_authors, [somef.somef_data, cd.codemeta_data, cf.cff_data]),
                (rt.test_contributors, [somef.somef_data, cd.codemeta_data]),
                (rt.test_authors_orcids, [cd.codemeta_data, cf.cff_data]),
                (rt.test_author_roles, [cd.codemeta_data]),
                (rt.test_metadata_exists, [somef.somef_data, cd.codemeta_data, cf.cff_data]),
                (rt.test_codemeta_exists, [cd.codemeta_data]),
                (rt.test_descriptive_metadata, [somef.somef_data]),
                (rt.test_title_description, [somef.somef_data]),
                (rt.test_version_number_in_metadata, [somef.somef_data, cd.codemeta_data, cf.cff_data])
            ],
            "software_has_citation": [
                (rt.test_has_citation, [somef.somef_data]),
                (rt.test_reference_publication, [somef.somef_data, cd.codemeta_data])
            ],
            "software_documentation": [
                (rt.test_software_documentation, [somef.somef_data]),
                (rt.test_readme_exists, [somef.somef_data]),
                (rt.test_contact_support_documentation, [somef.somef_data]),
                (rt.test_installation_instructions, [somef.somef_data])
            ],
            "archived_in_software_heritage": [
                (rt.test_metadata_record_in_zenodo_or_software_heritage, [somef.somef_data])
            ]
        }
        
    def assess_indicators(self):
        results = []
        for id in self.indicator_functions:
            for func, args in self.indicator_functions[id]:
                result = func(*args)
                results.append(result)
            
        return results
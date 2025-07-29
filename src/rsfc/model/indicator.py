from rsfc.rsfc_tests import rsfc_tests as rt

class Indicator:
    
    def __init__(self, sw, somef):
        
        self.indicator_functions = {
            "persistent_and_unique_identifier": [
                (rt.test_id_presence_and_resolves, [somef.somef_data]),
                (rt.test_id_proper_schema, [somef.somef_data]),
                (rt.test_id_associated_with_software, [somef.somef_data, sw.url, sw.repo_type, sw.repo_branch]),
                (rt.test_identifier_in_readme_citation, [somef.somef_data]),
                (rt.test_identifier_resolves_to_software, [somef.somef_data])
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
                (rt.test_presence_of_tests, [sw.url, sw.repo_type, sw.repo_branch])
            ],
            "repository_workflows": [
                (rt.test_github_action_tests, [somef.somef_data]),
                (rt.test_repository_workflows, [somef.somef_data])
            ],
            "version_control_use": [
                (rt.test_is_github_repository, [sw.url]),
                (rt.test_repo_enabled_and_commits, [somef.somef_data, sw.url, sw.repo_type, sw.repo_branch]),
                (rt.test_repo_status, [somef.somef_data])
            ],
            "software_has_license": [
                (rt.test_has_license, [somef.somef_data]),
                (rt.test_license_spdx_compliant, [somef.somef_data]),
                (rt.test_license_info_in_metadata_files, [somef.somef_data, sw.url, sw.repo_type, sw.repo_branch])
            ],
            "descriptive_metadata": [
                (rt.test_authors_contribs, [somef.somef_data]),
                (rt.test_authors_orcids, [somef.somef_data]),
                (rt.test_author_roles, [sw.url, sw.repo_type, sw.repo_branch]),
                (rt.test_metadata_exists, [somef.somef_data, sw.url, sw.repo_type, sw.repo_branch]),
                (rt.test_codemeta_exists, [sw.url, sw.repo_type, sw.repo_branch]),
                (rt.test_descriptive_metadata, [somef.somef_data]),
                (rt.test_title_description, [somef.somef_data])
            ],
            "software_has_citation": [
                (rt.test_has_citation, [somef.somef_data]),
                (rt.test_reference_publication, [somef.somef_data, sw.url, sw.repo_type, sw.repo_branch])
            ],
            "software_documentation": [
                (rt.test_software_documentation, [somef.somef_data]),
                (rt.test_readme_exists, [somef.somef_data]),
                (rt.test_contact_support_documentation, [somef.somef_data]),
                (rt.test_installation_instructions, [somef.somef_data])
            ]
        }
        
    def assess_indicators(self):
        results = []
        for id in self.indicator_functions:
            for func, args in self.indicator_functions[id]:
                result = func(*args)
                results.append(result)
            
        return results
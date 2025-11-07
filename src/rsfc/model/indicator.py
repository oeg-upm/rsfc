from rsfc.rsfc_tests import rsfc_tests as rt

class Indicator:
    
    def __init__(self, somef, cd, cf, gh):

        self.test_functions = {
            "RSFC-01": [
                (rt.test_id_presence_and_resolves, [somef.somef_data]),
                (rt.test_id_associated_with_software, [somef.somef_data, cd.codemeta_data, cf.cff_data]),
                (rt.test_id_common_schema, [somef.somef_data])
            ],
            "RSFC-03": [
                (rt.test_has_releases, [somef.somef_data]),
                (rt.test_release_id_and_version, [somef.somef_data]),
                (rt.test_semantic_versioning_standard, [somef.somef_data]),
                (rt.test_version_scheme, [somef.somef_data]),
                (rt.test_latest_release_consistency, [somef.somef_data]),
                (rt.test_version_number_in_metadata, [somef.somef_data, cd.codemeta_data, cf.cff_data])
            ],
            "RSFC-04": [
                (rt.test_metadata_exists, [somef.somef_data, cd.codemeta_data, cf.cff_data]),
                (rt.test_readme_exists, [somef.somef_data]),
                (rt.test_title_description, [somef.somef_data]),
                (rt.test_descriptive_metadata, [somef.somef_data]),
                (rt.test_codemeta_exists, [cd.codemeta_data])
            ],
            "RSFC-05": [
                (rt.test_repo_status, [somef.somef_data]),
                (rt.test_contact_support_documentation, [somef.somef_data]),
                (rt.test_software_documentation, [somef.somef_data])
            ],
            "RSFC-06": [
                (rt.test_authors, [somef.somef_data, cd.codemeta_data, cf.cff_data]),
                (rt.test_contributors, [somef.somef_data, cd.codemeta_data]),
                (rt.test_authors_orcids, [cd.codemeta_data, cf.cff_data]),
                (rt.test_author_roles, [cd.codemeta_data])
            ],
            "RSFC-07": [
                (rt.test_identifier_in_readme_citation, [somef.somef_data, cf.cff_data]),
                (rt.test_identifier_resolves_to_software, [somef.somef_data, cd.codemeta_data, cf.cff_data, gh.repo_url])
            ],
            "RSFC-08": [
                (rt.test_metadata_record_in_zenodo_or_software_heritage, [somef.somef_data])
            ],
            "RSFC-09": [
                (rt.test_is_github_repository, [gh.repo_url])
            ],
            "RSFC-12": [
                (rt.test_reference_publication, [somef.somef_data, cd.codemeta_data])
            ],
            "RSFC-13": [
                (rt.test_dependencies_declared, [somef.somef_data]),
                (rt.test_installation_instructions, [somef.somef_data]),
                (rt.test_dependencies_have_version, [somef.somef_data]),
                (rt.test_dependencies_in_machine_readable_file, [somef.somef_data])
            ],
            "RSFC-14": [
                (rt.test_presence_of_tests, [gh]),
                (rt.test_github_action_tests, [somef.somef_data])
            ],
            "RSFC-15": [
                (rt.test_has_license, [somef.somef_data]),
                (rt.test_license_spdx_compliant, [somef.somef_data]),
                (rt.test_license_information_provided, [somef.somef_data])
            ],
            "RSFC-16": [
                (rt.test_license_info_in_metadata_files, [somef.somef_data, cd.codemeta_data, cf.cff_data])
            ],
            "RSFC-17": [
                (rt.test_repo_enabled_and_commits, [somef.somef_data, gh]),
                (rt.test_commit_history, [gh]),
                (rt.test_commits_linked_issues, [gh])
            ],
            "RSFC-18": [
                (rt.test_has_citation, [somef.somef_data])
            ],
            "RSFC-19": [
                (rt.test_repository_workflows, [somef.somef_data])
            ]
        }
        
    def assess_indicators(self):
        results = []
        for id in self.test_functions:
            for func, args in self.test_functions[id]:
                result = func(*args)
                results.append(result)
            
        return results
from rsfc.rsfc_tests import rsfc_tests as rt

class Indicator:
    
    def __init__(self, somef, cd, cf, gh):

        self.test_functions = {
            "RSFC-01-1": [
                (rt.test_id_presence_and_resolves, [somef.somef_data])
            ],
            "RSFC-01-2": [
                (rt.test_id_associated_with_software, [somef.somef_data, cd.codemeta_data, cf.cff_data])
            ],
            "RSFC-01-3": [
                (rt.test_id_common_schema, [somef.somef_data])
            ],
            "RSFC-03-1": [
                (rt.test_has_releases, [somef.somef_data])
            ],
            "RSFC-03-2": [
                (rt.test_release_id_and_version, [somef.somef_data])
            ],
            "RSFC-03-3": [
                (rt.test_semantic_versioning_standard, [somef.somef_data])
            ],
            "RSFC-03-4": [
                (rt.test_version_scheme, [somef.somef_data])
            ],
            "RSFC-03-5": [
                (rt.test_latest_release_consistency, [somef.somef_data])
            ],
            "RSFC-03-6": [
                (rt.test_version_number_in_metadata, [somef.somef_data, cd.codemeta_data, cf.cff_data])
            ],
            "RSFC-04-1": [
                (rt.test_metadata_exists, [somef.somef_data, cd.codemeta_data, cf.cff_data])
            ],
            "RSFC-04-2": [
                (rt.test_readme_exists, [somef.somef_data])
            ],
            "RSFC-04-3": [
                (rt.test_title_description, [somef.somef_data])
            ],
            "RSFC-04-4": [
                (rt.test_descriptive_metadata, [somef.somef_data])
            ],
            "RSFC-04-5": [
                (rt.test_codemeta_exists, [cd.codemeta_data])
            ],
            "RSFC-05-1": [
                (rt.test_repo_status, [somef.somef_data])
            ],
            "RSFC-05-2": [
                (rt.test_contact_support_documentation, [somef.somef_data])
            ],
            "RSFC-05-3": [
                (rt.test_software_documentation, [somef.somef_data])
            ],
            "RSFC-06-1": [
                (rt.test_authors, [somef.somef_data, cd.codemeta_data, cf.cff_data])
            ],
            "RSFC-06-2": [
                (rt.test_contributors, [somef.somef_data, cd.codemeta_data])
            ],
            "RSFC-06-3": [
                (rt.test_authors_orcids, [cd.codemeta_data, cf.cff_data])
            ],
            "RSFC-06-4": [
                (rt.test_author_roles, [cd.codemeta_data])
            ],
            "RSFC-07-1": [
                (rt.test_identifier_in_readme_citation, [somef.somef_data, cf.cff_data])
            ],
            "RSFC-07-2": [
                (rt.test_identifier_resolves_to_software, [somef.somef_data, cd.codemeta_data, cf.cff_data, gh.repo_url])
            ],
            "RSFC-08-1": [
                (rt.test_metadata_record_in_zenodo_or_software_heritage, [somef.somef_data])
            ],
            "RSFC-09-1": [
                (rt.test_is_github_repository, [gh.repo_url])
            ],
            "RSFC-12-1": [
                (rt.test_reference_publication, [somef.somef_data, cd.codemeta_data])
            ],
            "RSFC-13-1": [
                (rt.test_dependencies_declared, [somef.somef_data])
            ],
            "RSFC-13-2": [
                (rt.test_installation_instructions, [somef.somef_data])
            ],
            "RSFC-13-3": [
                (rt.test_dependencies_have_version, [somef.somef_data])
            ],
            "RSFC-13-4": [
                (rt.test_dependencies_in_machine_readable_file, [somef.somef_data])
            ],
            "RSFC-14-1": [
                (rt.test_presence_of_tests, [gh])
            ],
            "RSFC-14-2": [
                (rt.test_github_action_tests, [somef.somef_data])
            ],
            "RSFC-15-1": [
                (rt.test_has_license, [somef.somef_data])
            ],
            "RSFC-15-2": [
                (rt.test_license_spdx_compliant, [somef.somef_data])
            ],
            "RSFC-15-3": [
                (rt.test_license_information_provided, [somef.somef_data])
            ],
            "RSFC-16-1": [
                (rt.test_license_info_in_metadata_files, [somef.somef_data, cd.codemeta_data, cf.cff_data])
            ],
            "RSFC-17-1": [
                (rt.test_repo_enabled_and_commits, [somef.somef_data, gh])
            ],
            "RSFC-17-2": [
                (rt.test_commit_history, [gh])
            ],
            "RSFC-17-3": [
                (rt.test_commits_linked_issues, [gh])
            ],
            "RSFC-18-1": [
                (rt.test_has_citation, [somef.somef_data])
            ],
            "RSFC-19-1": [
                (rt.test_repository_workflows, [somef.somef_data])
            ]
        }
        
    def assess_indicators(self, test_id):
        results = []
        if test_id != None:
            func, args = self.test_functions[test_id][0]
            result = func(*args)
            results.append(result)
        else:
            for id in self.test_functions:
                for func, args in self.test_functions[id]:
                    result = func(*args)
                    results.append(result)
            
        return results
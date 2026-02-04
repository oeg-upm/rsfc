import argparse

def main():
    parser = argparse.ArgumentParser(description="RSFC - EVERSE Research Software Fairness Checks")
    parser.add_argument("--repo", required=True, help="URL of the Github/Gitlab repository to be analyzed")
    parser.add_argument("--ftr", action="store_true", help="Flag to indicate if JSON-LD in FTR format is desired")
    parser.add_argument("--id", required=False, help="Identifier of a specific test. Only that test will be ran")
    parser.add_argument("-t", required=False, help="Authorization Github token")

    args = parser.parse_args()
    
    print("Making preparations...")
    
    from rsfc.rsfc_core import start_assessment
    from rsfc.utils.rsfc_helpers import resolve_w3id, remove_git_from_url
    import os
    import json
    
    print("Checking if url is w3id")
    
    repo_url = resolve_w3id(args.repo)
    repo_url = remove_git_from_url(repo_url)
    
    rsfc_asmt, table = start_assessment(repo_url, args.ftr, args.id, args.t)
    
    output_dir = './rsfc_output/'
    output_file = "rsfc_assessment.json"
    output_path = os.path.join(output_dir, output_file)
    
    print("Saving assessment locally...")
    
    os.makedirs(output_dir, exist_ok=True)

    if os.path.exists(output_path):
        os.remove(output_path)

    with open(output_path, 'w') as f:
        json.dump(rsfc_asmt, f, indent=4)
        
    print("Creating terminal output...")
    print(table)

if __name__ == "__main__":
    main()

import argparse

def main():
    parser = argparse.ArgumentParser(description="RSFC - EVERSE Research Software Fairness Checks")
    parser.add_argument("--repo", required=True, help="URL of the Github repository to be analyzed")

    args = parser.parse_args()
    
    print("Making preparations...")
    
    from rsfc.rsfc_core import start_assessment
    import os
    import json
    
    rsfc_asmt, table = start_assessment(args.repo)
    
    output_path = './outputs/rsfc_assessment.json'
    print("Saving assessment locally...")

    if os.path.exists(output_path):
        os.remove(output_path)

    with open(output_path, 'w') as f:
        json.dump(rsfc_asmt, f, indent=4)
        
    print("Creating terminal output...")
    print(table)

if __name__ == "__main__":
    main()

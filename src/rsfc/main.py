import argparse

def main():
    parser = argparse.ArgumentParser(description="RSFC - EVERSE Research Software Fairness Checks")
    parser.add_argument("repo_url", help="URL of the Github repository to be analyzed")

    args = parser.parse_args()
    
    from rsfc.rsfc_core import build_assessment
    build_assessment(args.repo_url)

if __name__ == "__main__":
    main()

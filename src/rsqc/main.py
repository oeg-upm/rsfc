import argparse

def main():
    parser = argparse.ArgumentParser(description="RSQC - EVERSE Research Software Quality Checks")
    parser.add_argument("repo_url", help="URL of the Github repository to be analyzed")

    args = parser.parse_args()
    
    from rsqc.rsqc_core import build_assessment
    build_assessment(args.repo_url)

if __name__ == "__main__":
    main()

import os
import json
import sys
import click

@click.command(help="RSFC - EVERSE Research Software Fairness Checks")
@click.option('--repo', help="URL of the Github/Gitlab repository to be analyzed")
@click.option('--local', type=click.Path(exists=True, file_okay=False), help="Local path of the repository to be analyzed")
@click.option('-b', help="Name of the repo branch to analyze. By default main/master")
@click.option('-v', help="Tag of the release to analyze. By default latest release.")
@click.option('--ftr', is_flag=True, help="Flag to indicate if JSON-LD in FTR format is desired")
@click.option('--id', help="Identifier of a specific test. Only that test will be ran")
@click.option('--metadata', type=click.Path(exists=True, dir_okay=False), help="SOMEF metadata file in case you already have one")
@click.option('-t', help="Authorization Github token")
@click.option('-s', is_flag=True, help="Flag to indicate if SOMEFs output is to be saved locally")
def main(repo, local, b, v, ftr, id, metadata, t, s):

    if local:
        if repo:
            raise click.UsageError("You can't use '--repo' and '--local' at the same time.")
        if b or v or t:
            raise click.UsageError("Remote options ('-b', '-v', '-t') cannot be used with '--local'.")
            
    if not repo and not local:
        raise click.UsageError("Either '--repo' or '--local' must be passed.")

    if b and v:
        raise click.UsageError("You can't use '-b' and '-v' at the same time.")

    click.echo("Making preparations...")
    
    from rsfc.rsfc_core import start_assessment
    from rsfc.utils.rsfc_helpers import resolve_w3id, remove_git_from_url
    from rsfc.utils.exceptions import GithubRateLimitExceeded
    
    if repo:
        click.echo("Checking if url is w3id")
        target = resolve_w3id(repo)
        target = remove_git_from_url(target)
        mode = "remote"
    else:
        target = local
        mode = "local"
    
    try:
        rsfc_asmt, table = start_assessment(target, b, v, ftr, id, metadata, t, s, mode)
        
    except GithubRateLimitExceeded as e:
        click.echo(click.style(f"\nERROR: {e}", fg="red"), err=True)
        click.echo("If you want to keep using RSFC, please use a Github token. More information available in this project's README file.")
        sys.exit(1)
    
    output_dir = './rsfc_output/'
    output_file = "rsfc_assessment.json"
    output_path = os.path.join(output_dir, output_file)
    
    click.echo("Saving assessment locally...")
    os.makedirs(output_dir, exist_ok=True)

    if os.path.exists(output_path):
        os.remove(output_path)

    with open(output_path, 'w') as f:
        json.dump(rsfc_asmt, f, indent=4)
        
    click.echo("Creating terminal output...")
    click.echo(table)

if __name__ == "__main__":
    main()
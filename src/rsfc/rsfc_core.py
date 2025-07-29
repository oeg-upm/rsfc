import os
import json
from rsfc.model import assessedSoftware as soft
from rsfc.model import indicator as ind
from rsfc.model import assessment as asmt
from rsfc.harvesters import somef_harvester as som


def start_assessment(repo_url):
    
    sw = soft.AssessedSoftware(repo_url)
    somef = som.SomefExtractor(repo_url)
    
    print("Assessing repository...")

    indi = ind.Indicator(sw, somef)
    checks = indi.assess_indicators()
    
    assess = asmt.Assessment(checks)
    
    print("Saving assessment locally...")
    rsfc_asmt = assess.render_template(sw)
    output_path = './outputs/rsfc_assessment.json'

    if os.path.exists(output_path):
        os.remove(output_path)

    with open(output_path, 'w') as f:
        json.dump(rsfc_asmt, f, indent=4)
    
    table = assess.to_terminal_table()
    print("Creating terminal output...")
    print(table)

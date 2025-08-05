import os
import json
from rsfc.model import assessedSoftware as soft
from rsfc.model import indicator as ind
from rsfc.model import assessment as asmt
from rsfc.harvesters import somef_harvester as som
from rsfc.harvesters import codemeta_harvester as cm
from rsfc.harvesters import cff_harvester as cf


def start_assessment(repo_url):
    
    sw = soft.AssessedSoftware(repo_url)
    somef = som.SomefHarvester(repo_url)
    code = cm.CodemetaHarvester(sw)
    cff = cf.CFFHarvester(sw)
    
    print("Assessing repository...")

    indi = ind.Indicator(sw, somef, code, cff)
    checks = indi.assess_indicators()
    
    assess = asmt.Assessment(checks)
    
    rsfc_asmt = assess.render_template(sw)
    output_path = './outputs/rsfc_assessment.json'
    
    print("Saving assessment locally...")

    if os.path.exists(output_path):
        os.remove(output_path)

    with open(output_path, 'w') as f:
        json.dump(rsfc_asmt, f, indent=4)
    
    table = assess.to_terminal_table()
    print("Creating terminal output...")
    print(table)

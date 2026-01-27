from tabulate import tabulate
from jinja2 import Environment, BaseLoader
from datetime import datetime, timezone
import json
from importlib.resources import files
from rsfc.utils import constants
import uuid

class Assessment:
    def __init__(self, checks):
        self.checks = checks
        

    def render_template(self, sw, ftr, test_id):
        
        print("Rendering assessment...")
        
        data = dict()
        data['name'] = sw.name
        data['url'] = sw.url
        data['version'] = sw.version
        data['doi'] = sw.id
        
        if ftr and test_id:
            data['check'] = self.checks[0]
            data['result_id'] = f"urn:rsfc:{uuid.uuid4()}"
        else:
            data['checks'] = self.checks
            
        now = datetime.now(timezone.utc)
        data.setdefault("date", str(now.date()))
        data.setdefault("date_iso", now.replace(microsecond=0).isoformat().replace('+00:00', 'Z'))
        
        if ftr and test_id:
            with files("rsfc").joinpath("templates/assessment_schema_ftr_single.json.j2").open("r", encoding="utf-8") as f:
                template_source = f.read()
        elif ftr:
            with files("rsfc").joinpath("templates/assessment_schema_ftr.json.j2").open("r", encoding="utf-8") as f:
                template_source = f.read()
        else:
            with files("rsfc").joinpath("templates/assessment_schema.json.j2").open("r", encoding="utf-8") as f:
                template_source = f.read()

        env = Environment(loader=BaseLoader(), trim_blocks=True, lstrip_blocks=True)
        template = env.from_string(template_source)

        rendered = template.render(**data)
        
        return json.loads(rendered)
    
    
    def to_terminal_table(self, test_id):
        rows = []
        
        for check in self.checks:
            if test_id != None:
                if test_id in check["test_id"]:
                    desc = constants.TEST_DESC_DICT.get(check["test_id"], "None")
                    
                    rows.append([
                        check["test_id"],
                        desc,
                        str(check["output"])
                    ])
            else:
                desc = constants.TEST_DESC_DICT.get(check["test_id"], "None")
                
                rows.append([
                    check["test_id"],
                    desc,
                    str(check["output"])
                ])

        headers = ["TEST ID", "Short Description", "Output"]
        table = tabulate(rows, headers, tablefmt="grid")
        info = "\n\nFor rationale on the tests performed, please check the assessment file created in the outputs folder.\n"
        table = table + info
        
        return table
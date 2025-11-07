from tabulate import tabulate
from jinja2 import Environment, BaseLoader
from datetime import datetime, timezone
import json
from importlib.resources import files
from rsfc.utils import constants

class Assessment:
    def __init__(self, checks):
        self.checks = checks
        

    def render_template(self, sw):
        
        print("Rendering assessment...")
        
        data = dict()
        
        data['name'] = sw.name
        data['url'] = sw.url
        data['version'] = sw.version
        data['doi'] = sw.id
        data['checks'] = self.checks
        
        with files("rsfc").joinpath("templates/assessment_schema.json.j2").open("r", encoding="utf-8") as f:
            template_source = f.read()

        env = Environment(loader=BaseLoader(), trim_blocks=True, lstrip_blocks=True)
        template = env.from_string(template_source)

        now = datetime.now(timezone.utc)
        data.setdefault("date", str(now.date()))
        data.setdefault("date_iso", now.replace(microsecond=0).isoformat().replace('+00:00', 'Z'))

        rendered = template.render(**data)
        
        return json.loads(rendered)
    
    
    def to_terminal_table(self):
        rows = []
        
        for i, check in enumerate(self.checks):
            desc = constants.TEST_DESC_LIST[i] if i < len(constants.TEST_DESC_LIST) else "None"
            
            rows.append([
                check["test_id"],
                desc,
                str(check["output"])
            ])

        headers = ["TEST ID", "Short Description", "Output"]
        table = tabulate(rows, headers, tablefmt="grid")
        info = "\n\nFor rationale on the tests performed, please check the assessment file created in the outputs folder.\n"
        table = table +info
        
        return table
        
        
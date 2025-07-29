from tabulate import tabulate
from jinja2 import Environment, BaseLoader
from datetime import datetime, timezone
import json
from importlib.resources import files

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
        
        for check in self.checks:
            rows.append([
                check["assessesIndicator"]["@id"],
                check["status"]["@id"].split(":")[-1],
                str(check["output"]),
                str(check["evidence"])
            ])

        headers = ["Indicator ID", "Status", "Output", "Evidence"]
        table = tabulate(rows, headers, tablefmt="grid")
        
        return table
        
        
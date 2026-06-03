from collections import Counter, defaultdict
from rsfc.utils import constants

class MarkdownReportGenerator:
    
    def __init__(self, asmt, table):
        self.table = table

        if "checks" in asmt:
            self.data = asmt
            self.checks = asmt.get("checks", [])

        elif "hadMember" in asmt:
            self.data = self.normalize_ftr_metadata(asmt)
            self.checks = self.normalize_ftr_checks(asmt.get("hadMember", []))

        else:
            self.data = asmt
            self.checks = []
        

    @staticmethod
    def status_value(check):
        raw = str(check.get("output", "unknown")).strip().lower()
        return constants.STATUS_MAP_REPORT.get(raw, raw)

    @staticmethod
    def indicator_name(check):
        indicator = check.get("assessesIndicator", {})
        return indicator.get("@id", "unknown").split("/")[-1]

    @staticmethod
    def escape_html(text):
        text = str(text)
        return (
            text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
        )

    @staticmethod
    def make_anchor(text: str) -> str:
        anchor = str(text).strip().lower()
        for ch in [" ", "/", ".", ":"]:
            anchor = anchor.replace(ch, "-")
        return anchor

    @staticmethod
    def row_color(output: str) -> str:
        output = str(output).strip().lower()
        if output == "true":
            return "#d4edda"
        if output == "false":
            return "#f8d7da"
        return "#fff3cd"



    def compute_counts(self):
        return Counter(self.status_value(c) for c in self.checks)

    def group_by_indicator(self):
        grouped = defaultdict(list)
        for check in self.checks:
            grouped[self.indicator_name(check)].append(check)
        return grouped


    def header_section(self):
        name = self.data.get("name", "Software Quality Assessment")
        description = self.data.get("description", "")

        md = [f"# {name}\n"]
        if description:
            md.append(f"{description}\n")
        return md

    def general_info_section(self):
        assessed = self.data.get("assessedSoftware", {})
        software_name = assessed.get("name", "unknown")
        software_url = assessed.get("url", "")
        date_created = self.data.get("dateCreated", "unknown")

        md = ["## General Information\n"]
        md.append(f"- **Software:** {software_name}")
        if software_url:
            md.append(f"- **Repository:** {software_url}")
        md.append(f"- **Assessment date:** {date_created}")
        md.append(f"- **Total checks:** {len(self.checks)}\n")
        return md

    def summary_section(self, counts):
        md = ["## Summary\n"]
        md.append(f"- **Passed (`true`)**: {counts.get('true', 0)}")
        md.append(f"- **Failed (`false`)**: {counts.get('false', 0)}")
        md.append(f"- **Errors (`error`)**: {counts.get('error', 0)}\n")
        return md

    def results_table_section(self):

        md = ["## Results Table\n"]
        md.append("```text")
        md.append(self.table.strip())
        md.append("```\n")

        return md

    def detailed_section(self, grouped):
        md = ["## Detailed Results by Indicator\n"]

        for ind in sorted(grouped):
            md.append(f"### {ind}\n")

            for check in grouped[ind]:
                anchor = self.make_anchor(f"{ind}-{check.get('test_id', '')}")

                md.extend([
                    f'<a id="{anchor}"></a>',
                    f"#### {check.get('test_name', 'Unnamed test')}\n",
                    f"- **Test ID:** {check.get('test_id', '')}",
                    f"- **Result:** {self.status_value(check)}",
                    f"- **Process:** {check.get('process', 'N/A')}",
                    f"- **Evidence:** {check.get('evidence', 'N/A')}",
                    f"- **Suggestions:** {check.get('suggestions', 'N/A')}\n",
                ])

        return md
    
    
    def normalize_ftr_metadata(self, data):

        normalized = {}

        normalized["name"] = (
            data.get("title") or "Software Quality Assessment"
        )

        normalized["description"] = data.get("description", "")

        normalized["dateCreated"] = (
            data.get("generatedAtTime", {}).get("@value", "unknown")
        )

        target = data.get("assessmentTarget", {})

        normalized["assessedSoftware"] = {
            "name": target.get("title", "unknown"),
            "url": target.get("url", "")
        }

        return normalized
    
    
    def normalize_ftr_checks(self, members):

        checks = []

        for m in members:
            test = m.get("outputFromTest", {})
            metric = m.get("hasAssociatedMetric", {})

            test_id = test.get("@id", "")
            if "/" in test_id:
                test_id = test_id.split("/")[-1]

            checks.append({
                "test_id": test_id,
                "test_name": test.get("title", ""),
                "output": m.get("value", "unknown"),
                "process": test.get("description", ""),
                "evidence": m.get("log", m.get("description", "")),
                "suggestions": m.get("suggestion", ""),
                "assessesIndicator": {
                    "@id": metric.get("@id", "unknown")
                }
            })

        return checks
    
    
    def table_to_markdown(self):

        lines = self.table.strip().splitlines()

        rows = []

        for line in lines:
            line = line.strip()

            if line.startswith("For rationale on the tests performed"):
                break

            if line.startswith("+"):
                continue

            if line.startswith("|"):
                cells = [cell.strip() for cell in line.strip("|").split("|")]
                rows.append(cells)

        if not rows:
            return ""

        header = rows[0]
        data_rows = rows[1:]

        md = []

        md.append("| " + " | ".join(header) + " |")

        md.append("| " + " | ".join(["---"] * len(header)) + " |")

        for row in data_rows:
            md.append("| " + " | ".join(row) + " |")

        return "\n".join(md)
    
    
    def results_table_section(self):

        md = ["## Results Table\n"]

        markdown_table = self.table_to_markdown()

        md.append(markdown_table + "\n")

        return md


    def generate(self, output_path):
        counts = self.compute_counts()
        grouped = self.group_by_indicator()

        md = []
        md.extend(self.header_section())
        md.extend(self.general_info_section())
        md.extend(self.summary_section(counts))
        md.extend(self.results_table_section())
        md.extend(self.detailed_section(grouped))

        content = "\n".join(md)

        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)

        return content
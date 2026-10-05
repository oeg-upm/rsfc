from rsfc.model import assessment as asmt
from rsfc.model import executionContext as ctx
from rsfc.model import rsfcEvaluator as eval
from rsfc.model import markdownReportGenerator as mdRep
from rsfc.utils import rsfc_helpers


def start_assessment(repo, branch, tag, ftr, test_id, metadata, token, s, mode):
    
    context = ctx.ExecutionContext(repo, branch, tag, metadata, token, s, mode)
    evaluator = eval.RSFCEvaluator(context.get_context())
    evaluator.assess_indicators(test_id)
    checks = evaluator.get_results()
    
    assess = asmt.Assessment(checks)
    badge_url = rsfc_helpers.generate_badge(checks)
    
    rsfc_asmt = assess.render_template(context.get_context(), ftr, test_id)
    table, info, badge = assess.to_terminal_table(test_id, badge_url)
    report = mdRep.MarkdownReportGenerator(rsfc_asmt, table)
    report.generate("./RSFC_REPORT.md")
    if test_id != None:
        table = table + info
    else:
        table = table + info + badge
    
    return rsfc_asmt, table

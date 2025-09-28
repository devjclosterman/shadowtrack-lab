from jinja2 import Environment, FileSystemLoader
import os

env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")))

def render_html_report(report: dict, out_path: str):
    tpl = env.get_template("report.html")
    html = tpl.render(report=report)
    with open(out_path, "w", encoding='utf-8') as f:
        f.write(html)

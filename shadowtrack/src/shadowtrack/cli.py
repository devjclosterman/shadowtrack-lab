import click
from .scanner import check_email_local, extract_exif, scan_text_for_secrets
from .reporters import render_html_report
import os, glob

@click.group()
def cli(): pass

@cli.command()
@click.option("--email", help="Email to scan", required=False)
@click.option("--images", help="Folder with images to scan", required=False)
@click.option("--code", help="Folder with code files to scan", required=False)
@click.option("--out", default="shadowtrack_report.html", help="Output HTML report")
def scan(email, images, code, out):
    report = {"email": None, "images": [], "secrets": []}
    if email:
        breaches = check_email_local(email)
        report["email"] = {"address": email, "breaches": breaches}
    if images:
        image_paths = glob.glob(os.path.join(images, "*"))
        for p in image_paths:
            try:
                exif = extract_exif(p)
                report["images"].append({"path": p, "exif": exif})
            except Exception as e:
                report["images"].append({"path": p, "error": str(e)})
    if code:
        for root, _, files in os.walk(code):
            for f in files:
                path = os.path.join(root, f)
                try:
                    with open(path, "r", errors="ignore") as fh:
                        txt = fh.read()
                    secrets = scan_text_for_secrets(txt)
                    if secrets:
                        report["secrets"].append({"path": path, "matches": secrets})
                except Exception as e:
                    continue
    render_html_report(report, out)
    click.echo(f"Report written to {out}")

if __name__ == "__main__":
    cli()

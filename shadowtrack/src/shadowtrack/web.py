from flask import Flask, request, send_file
from .reporters import render_html_report
from .scanner import check_email_local, extract_exif
import tempfile, os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), "templates"))

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        email = request.form.get("email")
        report = {"email": None, "images": [], "secrets": []}
        if email:
            report["email"] = {"address": email, "breaches": check_email_local(email)}
        imgdir = os.path.abspath(os.path.join(os.getcwd(), "examples", "images"))
        if os.path.isdir(imgdir):
            for fname in os.listdir(imgdir):
                path = os.path.join(imgdir, fname)
                try:
                    report["images"].append({"path": path, "exif": extract_exif(path)})
                except Exception:
                    pass
        out = os.path.join(tempfile.gettempdir(), "shadowtrack_report.html")
        render_html_report(report, out)
        return send_file(out)
    return '''
      <h1>ShadowTrack</h1>
      <form method="post">
        Email to scan: <input name="email" /><br/>
        <button type="submit">Run Quick Scan</button>
      </form>
    '''

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)

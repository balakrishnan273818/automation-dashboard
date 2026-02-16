from flask import Flask, render_template
from data import projects, org_summary

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/")
def coverage():
    return render_template(
        "index.html",
        projects=projects,
        org_summary=org_summary)

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template
from data import projects

app = Flask(__name__)

@app.route("/")
def coverage():
    return render_template("index.html", projects=projects)

if __name__ == "__main__":
    app.run(debug=True)
## Simple HTTP Server project

from flask import Flask, render_template
import json


app = Flask(__name__)

def load_projects():
    with open("projects.json", "r") as f:
        return json.load(f)

##Home page
@app.route('/')
def home():
    projects = load_projects()

    return render_template("index.html", title="Home - My Flask App", author="ME", projects=projects)

#about page
@app.route('/about')
def about():
    return render_template("about.html", title="About - My Flask App")

@app.route('/projects')
def projects():
    project_data = load_projects()
    return render_template("projects.html", title="Projects - My Flask App", projects=project_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

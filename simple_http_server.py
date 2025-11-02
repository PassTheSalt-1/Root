## Simple HTTP Server project

from flask import Flask, render_template
app = Flask(__name__)


project_list = [
    {"name": "Mini HTTP Server", "description": "A simple Flask-based web sever.", "url": "https://github.com/PassTheSalt-1/Root"},
    {"name": "System Info Script", "description": "Collects system info using Bash.", "url": "https://github.com/PassTheSalt-1/Root"},
    {"name": "Azure Funtions Demo", "description": "Explores serverless app integration.", "url": "https://github.com/PassTheSalt-1/Root"}
]


##Home page
@app.route('/')
def home():

    page_title = "Home - My Flask App"
    author = "ME"



    return render_template("index.html", title="Home - My Flask App", author="ME", projects=project_list )

#about page
@app.route('/about')
def about():
    return render_template("about.html", title="About - My Flask App")

@app.route('/projects')
def projects():
    return render_template("projects.html", title="Projects - My Flask App", projects=project_list)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

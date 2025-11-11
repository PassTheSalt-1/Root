## Simple HTTP Server project

from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
import logging
from logging.handlers import RotatingFileHandler
import os
from functools import wraps



app = Flask(__name__)
app.secret_key = 'super_secret_key'


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'

    return response
###LOGGING--------------------------------------------------
if not os.path.exists('logs'):
    os.mkdir('logs')

log_file = os.path.join('logs','app.log')

handler = RotatingFileHandler(log_file, maxBytes = 10240, backupCount=5)
formatter = logging.Formatter(
    '%(asctime)s [%(levelname)s] %(message)s in %(pathname)s:%(lineno)d'
)

handler.setFormatter(formatter)
handler.setLevel(logging.INFO)

app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

app.logger.info("Flask application startup complete")


##Home page
@app.route('/')
def home():
    projects = load_projects()

    return render_template("index.html", title="Home - My Flask App", author="ME", projects=projects)

##Decorators -----------------------------------------------------------

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function




###--------------------------------------------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    app.logger.info("Login page accessed.")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        app.logger.info(f"Login attempt with username: {username}")

        if username == 'admin' and password == 'admin':
            session['username'] = username
            app.logger.info(f"Successful login with username: {username}")
            return redirect(url_for('projects'))
        else:
            flash('NAH AH AH', 'danger')
            app.logger.info(f"Unsuccessful login attempt with username: {username}")
            return redirect(url_for('login'))
    return render_template('login.html')


#about page
@app.route('/about')
@login_required

def about():
    return render_template("about.html", title="About - My Flask App")

@app.route('/projects')
@login_required

def projects():

    if 'username' not in session:
        flash('You must login first!', 'danger')
        app.logger.info(f"Unauthorized access attemped")
        return redirect(url_for('login'))
    username =session['username']
    project_data = load_projects()
    return render_template("projects.html", title="Projects - My Flask App", projects=project_data, username=username)


def load_projects():
    with open("projects.json", "r") as f:
        return json.load(f)

@app.route('/logout')
def logout():
    username = session.pop('username', None)
    app.logger.info(f"User {username} has logged out.")
    flash("You have been logged out!", 'info')
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

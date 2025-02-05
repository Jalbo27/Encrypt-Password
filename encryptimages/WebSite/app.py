from flask import render_template, Flask, request
from engine import Engine

app = Flask(__name__)
responder = Engine()

@app.route("/")
@app.route("/homepage/")
@app.route("/homepage/<name>")
def home_page(name=None):
    return render_template("homepage.html", account=name) 

@app.route('/homepage/upload', methods=['POST'])
def uploadPassword():
    error = None
    if request.method == 'POST':
        if (responder.valid_password(request.form.get('name'), request.form.get('username'), request.form.get('password'), request.form.get('uri'))):
            return render_template("homepage.html")
    else:
        return render_template("homepage.html/")

@app.route("/login")
def loginPage():
    return render_template("login.html")
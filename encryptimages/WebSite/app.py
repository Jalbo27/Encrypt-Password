from flask import Flask, render_template, request, redirect, url_for, make_response
from engine import Engine
from markupsafe import escape
import json

app = Flask(__name__)
responder = Engine()

password_dict = [{}]
index = 0

@app.route("/")
@app.route("/homepage/")
@app.route("/homepage/<string:name>")
def home_page(name=''):
    return render_template("homepage.html", account=escape(name)) 

@app.route("/homepage/upload/<password>", methods=['POST'])
def uploadPassword(password):
    req_pass = json.load(request.json)
    password_dict.append(
        {
        'name': req_pass['name'],
        'username': req_pass['username'],
        'password': req_pass['password'],
        'uri': req_pass['uri']
        }
    )
    name = password_dict['name']
    username = password_dict['username']
    password = password_dict['password']
    uri = password_dict['uri']
    if responder.sanityPassword(name, username, password, uri):
        return render_template("homepage.html/", newLine=password_dict)
    else:
        return render_template("homepage.html/")


@app.route("/login", methods=['GET', 'POST'])
def loginPage():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print("I'm here")
        if responder.account(username, password, False):
            print("I'm here")
            return  redirect(url_for("home_page", name=username))
    elif request.method == 'GET':
        return render_template("login.html/")
    

@app.route("/register")
def register():
    pass
    

@app.route("/logout")
def logoutPage():
    return render_template("logout.html/")


@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp
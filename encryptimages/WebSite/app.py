#import sys, os 
#sys.path.insert(0, os.getcwd()+"/.venv/lib/") 
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
#from flask_json import FlaskJSON, json_response, JsonError
from engine import Engine
from markupsafe import escape
import json

app = Flask(__name__)

responder = Engine()

password_dict = []
index = 0

@app.route("/")
@app.route("/homepage/")
@app.route("/homepage/<string:name>")
def home_page(name=''):
    return render_template("homepage.html", account=escape(name), id=len(password_dict)) 


@app.route("/homepage/", methods=['POST'])
def uploadPassword():
    print('i\'m here', request.json)
    #print(req_pass)
    password_dict.append(
        request.get_json()
    )
    print('i\'m here', password_dict)
    name = password_dict[-1]['name']
    username = password_dict[-1]['username']
    password = password_dict[-1]['password']
    uri = password_dict[-1]['uri']
    print(f'i\'m here name: {name} username: {username} password: {password} uri: {uri}')
    # name = request.form['name']
    # username = request.form['username']
    # password = request.form['password']
    # uri = request.form['uri']
    if responder.sanityPassword(name, username, password, uri):
        print('i\'m here inside sanity password function')
        #return jsonify(password_dict[-1], status=200, mimetype="application/json")
        return render_template("homepage.html/", newLine=password_dict, len=len(password_dict))
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
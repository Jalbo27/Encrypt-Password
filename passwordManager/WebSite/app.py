from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from engine import Engine
from markupsafe import escape
import db

app = Flask(__name__)

responder = Engine()
password_dict = []

@app.route("/")
@app.route("/homepage/")
@app.route("/homepage/<string:name>")
def home_page(name=''):
    return render_template("homepage.html", account=escape(name), id=len(password_dict)) 


@app.route("/homepage/", methods=['POST'])
def uploadPassword():
    password_dict.append(request.get_json())
    print('i\'m here', password_dict)
    #id += 1
    #password_dict[-1]['id'] = id
    name = password_dict[-1]['name']
    username = password_dict[-1]['username']
    password = password_dict[-1]['password']
    uri = password_dict[-1]['uri']
    if responder.sanityPassword(name, username, password, uri):
        print('i\'m here inside sanity password function')
        print('response sent')
        return jsonify(password_dict[-1])
    else:
        return render_template("homepage.html/")

### LOADS LOGIN PAGE --- METHOD = 'GET'
@app.route("/login", methods=['GET'])
def loginPage():
    print("I\'m inside loginPage function")    
    return render_template("login.html") 

### CREATE OR LOGIN AN ACCOUNT --- METHOD = 'POST'
@app.route("/login", methods=['POST'])
def login():
    print("I\'m inside login function")
    if(request.get_json() != None):
        username = request.get_json()['username']
        password = request.get_json()['password']
        if responder.account(username, password, False):
            return jsonify(render_template("homepage.html/", account=username))
        else:
            response = {'login': 'failed'}
            return jsonify(response)
    

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
import werkzeug.exceptions
from werkzeug.exceptions import HTTPException
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, render_template, request, make_response, jsonify, json
from flask.logging import default_handler
from logging.config import dictConfig
from engine import Engine
from markupsafe import escape
from __inspection__ import currentLine
import time

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '['f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}''] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
app.logger.removeHandler(default_handler)
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=10
)

responder = Engine()
password_dict = []


### LOADS HOMEPAGE PAGE --- METHOD = 'GET'
@app.route("/")
@app.route("/homepage/", methods=['GET'])
@app.route("/homepage/<string:account>", methods=['GET'])
def home_page(account=''):
    if account != '':
        password_dict = responder.getAllPasswords(account)
        print(currentLine("app"), password_dict)
        if(password_dict != []):
            return render_template("homepage.html", account=escape(account), passwords=password_dict)
        else:
            return render_template("homepage.html", account=escape(account))

    return render_template("homepage.html") 


### UPLOAD THE PASSWORD INTO TABLE --- METHOD = 'POST'
@app.route("/homepage/", methods=['POST'])
@app.route("/homepage/<string:account>", methods=['POST'])
def uploadPassword(account=''):
    if(request.is_json):
        print(currentLine("app"), "il JSON ricevuto è: ", request.get_json())
        if(account == ''):
            return jsonify({'message': 'You have not an account. You have to login before', 'status': 'failed'})
        
        ### CHECK THE ACTION: 'submit', 'delete', 'edit'
        if(request.get_json()['action'] == 'submit'):
            password_dict.append(request.get_json())
            if (responder.sanityPassword(password_dict[-1])):
                print(currentLine("app")," I\'m here password sanity check passed successfully")
                password_dict[-1]['id'] += 1
                del password_dict[-1]['action']
                if (responder.addPassword(account, password_dict[-1])):
                    print(password_dict[-1])
                    del password_dict[-1]['_id']
                    return jsonify({'message': 'password added successfully', 'code': 200, 'id': password_dict[-1]['id']})
                else:
                    return jsonify({'message': 'failed to load password or there are problems in some fields', 'code': 417})
            else:
                return jsonify({'message': 'failed to load password or there are problems in some fields', 'code': 417})
            
        ### DELETE: Delete password of the current account
        elif (request.get_json()['action'] == 'delete'):
            if responder.deletePassword(account, int(request.get_json()['id'])):
                print(currentLine("app"), "password deleted")
                return jsonify({'message':'password deleted successfully', 'code': 200})
            else:
                return jsonify({'message':'error to delete the password', 'code': 417})
            
        ### EDIT: Edit a password of the current account
        elif (request.get_json()['action'] == 'edit'):
            if responder.deletePassword(account, int(request.get_json()['id'])):
                return jsonify({'message':'password edited successfully', 'code': 200})
            else:
                return jsonify({'message':'error to edit the password', 'code': 417})
            
        ### Wrong request
        else:
            print(currentLine("app"), request.headers, "\n")
            print(currentLine("app"), " Bad request")
            return render_template("homepage.html")
    ### The request sent is not json media type
    else:
        print(currentLine("app"), request.headers, "\n")
        print(currentLine("app"), " It is not a json media type")
        return render_template("homepage.html")
    
    
### LOADS LOGIN PAGE --- METHOD = 'GET'
@app.route("/login", methods=['GET'])
def loginPage():
    print(currentLine("app")," I\'m inside loginPage function")    
    return render_template("login.html") 


### CREATE OR LOGIN AN ACCOUNT --- METHOD = 'POST'
@app.route("/login", methods=['POST'])
def login():
    print(currentLine("app"), " I\'m inside login function")
    if (request.is_json):
        print(currentLine("app"), request.get_json())
        try:
            if(request.get_json() != None):
                username = request.get_json()['username']
                password = request.get_json()['password']
                if responder.account(username, password, False):
                    print(currentLine("app"), " User logged")
                    return jsonify({"code": 200, "url": f"/homepage/{username}"})
                else:
                    print(currentLine("app"), " Login failed")
                    return jsonify({"code": 401, "message": "login failed"})
            else:
                print(currentLine("app"), " Failed request")
                return jsonify({"code": 401, "message": "login failed"})
        except Exception as error:
            print(currentLine("app"), error)
            return jsonify({"code": 401, "message": "login failed"})
    else:
        print(currentLine("app"), " It is not a json media type")
        return jsonify({"code": 401, "message": "login failed"})
            
            
### LOADS REFGISTER PAGE --- METHOD = 'GET'
@app.route("/register", methods=['GET'])
def registerPage():
    return render_template("register.html")
    
    
 ### SUBSCRIBE NEW USER TO DB --- METHOD = 'POST'
@app.route("/register", methods=['POST'])
def register():
    print(currentLine("app"), " I\'m inside subscribe function")
    if (request.is_json):
        print(currentLine("app"), request.headers)
        print(currentLine("app"), request.get_json())
        try:
            if(request.get_json() != None):
                username = request.get_json()['username']
                password = request.get_json()['password']
                if responder.account(username, password, True):
                    print(currentLine("app"), " User created")
                    return jsonify({"code": 200, "url": f"/homepage/"})
                else:
                    print(currentLine("app"), " Register failed")
                    return jsonify({"code": 401, 'message': 'register failed'})
            else:
                print(currentLine("app"), " Failed request")
                return render_template("register.html", check=False)
        except Exception as error:
            print(currentLine("app"), error)
            return render_template("register.html", check=False)
    else:
        print(currentLine("app"), " It is not a json media type")
        return render_template("register.html", check=False)
       
       
### LOADS LOGOUT PAGE --- METHOD = 'GET'
@app.route("/logout")
def logoutPage():
    return render_template("logout.html/")


### HANDLE OF STATUS CODE OF ERROR (400 AND 500)
@app.errorhandler(werkzeug.exceptions.NotFound)
def not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp

@app.errorhandler(werkzeug.exceptions.Forbidden)
def forbidden():
    errorHandler(403)


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

def errorHandler(error):
    return render_template("error.html", error=error)
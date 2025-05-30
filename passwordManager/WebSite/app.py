import string, random, werkzeug.exceptions, time
from datetime import timedelta
from werkzeug.exceptions import HTTPException
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, render_template, request, make_response, jsonify, json, url_for, redirect
from flask.logging import default_handler
from logging.config import dictConfig
from engine import Engine
from markupsafe import escape
from __inspection__ import currentLine
from flask_jwt_extended import create_access_token, get_csrf_token, get_jwt, get_jwt_identity, jwt_required, JWTManager, set_access_cookies, unset_jwt_cookies

time.tzset()
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

ACCESS_EXPIRES=timedelta(minutes=120)

app = Flask(__name__)
app.secret_key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(13))
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
app.logger.removeHandler(default_handler)

### CONFIGURATION FOR JWT CONTROL AND CSRF (Cross Site Request Forgery Options)
app.config["JWT_COOKIE_CSRF_PROTECT"] = True
app.config["JWT_SECRET_KEY"] = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(13))
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
app.config["JWT_COOKIE_SECURE"] = True # in https set this to true
app.config["JWT_COOKIE_SAMESITE"] = "None"
app.config["JWT_SESSION_COOKIE"] = False
app.config["JWT_CSRF_IN_COOKIES"] = True
app.config["JWT_ACCESS_CSRF_COOKIE_NAME"] = "csrf_access_token"
app.config["JWT_ACCESS_CSRF_HEADER_NAME"] = "X-CSRF-TOKEN"
app.config["JWT_ACCESS_PATH"] = "/"
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=False,
    SESSION_COOKIE_SAMESITE='None',
    PERMANENT_SESSION_LIFETIME=ACCESS_EXPIRES)

jwt = JWTManager(app)

engine = Engine()
password_dict = []


### THE TOKEN IS EXPIRED AND REDIRECTS TO LOGIN PAGE
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    print(currentLine("app", "EXPIRED_TOKEN"), "Token expired")
    return redirect(url_for("login", code=307)) #alert="You have been logged out because the session is terminated"), code=307)

### LOADS HOMEPAGE WINDOW --- METHOD = 'GET'
@app.route("/")
@app.route("/homepage/", methods=['GET'])
def homepage_Page():
    return render_template("homepage.html")


### LOADS HOMEPAGE WINDOW WITH AN AUTHENTICATED ACCOUNT --- METHOD = 'GET' 
@app.route("/homepage/<string:account>", methods=['GET'])
@jwt_required(optional=True)
def home_page(account=''):
    if account != '' and engine.account(False, account):
        try:
            current_user = get_jwt_identity()
            print(currentLine("app", "HOMEPAGE"), current_user)
            #print(currentLine("app"), "Il codice JWT dell'utente è: ",request.cookies.get('access_token_cookie'))
            if current_user == account and engine.checkJWT(request.cookies.get('access_token_cookie')):
                print(currentLine("app", "HOMEPAGE"), "Users match")
                password_dict = engine.getAllPasswords(account)
                if(password_dict != []):
                    print(currentLine("app", "HOMEPAGE"), "User has passwords")
                    return render_template("homepage.html", account=escape(account), passwords=password_dict)
                else:
                    print(currentLine("app", "HOMEPAGE"), f'The account {account} has no passwords')
                    return render_template("homepage.html", account=account)
            else:
                print(currentLine("app", "HOMEPAGE", "ERROR"), "Users do not match")
                return redirect(url_for("login"))
        except Exception as e:
            print(currentLine("app", "HOMEPAGE", "ERROR"), e)
            return redirect(url_for("login"))
    else:
        print(currentLine("app", "HOMEPAGE", "ERROR"), "Account not found")
        return redirect(url_for("login"))


### UPLOAD THE PASSWORD INTO TABLE --- METHOD = 'POST'
@app.route("/homepage/", methods=['POST'])
@app.route("/homepage/<string:account>", methods=['POST'])
@jwt_required()
def uploadPassword(account=''):
    if(request.is_json):
        print(currentLine("app", "HOMEPAGE"), "JSON received and is valid")
        if(account == ''):
            return jsonify({"message": "You have not an account. You have to login before", "code": 401}), 200
        response = None
        if (account == get_jwt_identity()):
            ### CHECK THE ACTION: 'submit', 'delete', 'edit'
            if(request.get_json()['action'] == 'submit'):
                password_dict.append(request.get_json())
                if (engine.sanityPassword(password_dict[-1])):
                    print(currentLine("app", "HOMEPAGE"),"Password sanity check passed successfully")
                    password_dict[-1]['id'] += 1
                    del password_dict[-1]['action']
                    if (engine.addPassword(account, password_dict[-1])):
                        del password_dict[-1]['_id']
                        #print(currentLine("app"), password_dict[-1])
                        return jsonify({"id": password_dict[-1]['id'], "message": "Password added successfully", "code": 200}), 200
                    else:
                        return jsonify({"message": "Failed to load password or there are problems in some fields", "code": 4117}), 200
                else:
                    return jsonify({"message": "Failed to load password or there are problems in some fields", "code": 4117}), 200
                
            ### DELETE: Delete password of the current account
            elif (request.get_json()['action'] == 'delete'):
                if engine.deletePassword(account, int(request.get_json()['id'])):
                    print(currentLine("app", "HOMEPAGE"), "password deleted")
                    return jsonify({"message": "Password deleted successfully", "code": 200}), 200
                else:
                    print(currentLine("app", "HOMEPAGE", "ERROR"), "Password was not delete")
                    return jsonify({"message": "Error to delete the password", "code": 400}), 200
            ### EDIT: Edit a password of the current account
            elif (request.get_json()['action'] == 'edit'):
                if engine.deletePassword(account, int(request.get_json()['id'])):
                    return jsonify({"message": "Password modified successfully", "code": 200}), 100
                else:
                    return jsonify({"message": "Error to modify the password", "code": 400}), 200
            ### Wrong request
            else:
                print(currentLine("app", "HOMEPAGE"), request.headers, "\n")
                print(currentLine("app", "HOMEPAGE", "ERROR"), "Bad request")
                return render_template("homepage.html")
        else:
            return jsonify({"message": "You have not an account. You have to login before", "code": 401}), 200
    ### The request sent is not json media type
    else:
        print(currentLine("app", "HOMEPAGE"), request.headers, "\n")
        print(currentLine("app", "HOMEPAGE", "ERROR"), "It is not a json media type")
        return render_template("homepage.html")
    
    
### LOADS LOGIN PAGE --- METHOD = 'GET'
@app.route("/login", methods=['GET'])
def loginPage(alert=''):
    print(currentLine("app", "LOGIN"),"Login page rendered")    
    if alert != '': return render_template("login.html", alert=alert)
    else: return render_template("login.html")


### CREATE OR LOGIN AN ACCOUNT --- METHOD = 'POST'
@app.route("/login", methods=['POST'])
@jwt_required(optional=True)
def login():
    print(currentLine("app", "LOGIN"), "User is trying to login")
    if (request.is_json):
        print(currentLine("app", "LOGIN"), request.get_json())
        try:
            if(request.get_json() != None):
                username = request.get_json()['username']
                password = request.get_json()['password']
                ### CHECK IF USER EXISTS
                if engine.account(False, username, password=password):
                    ### CREATING A JWT TOKEN
                    used_token = request.cookies.get('access_token_cookie')
                    access_token = create_access_token(identity=username, expires_delta=ACCESS_EXPIRES)
                    print(currentLine("app", "LOGIN"), "Token created")
                    resp = jsonify({"access_token": access_token, "message": "login success", "code": 200})
                    set_access_cookies(response=resp, encoded_access_token=access_token)

                    if used_token is None:
                        print(currentLine("app", "LOGIN"), "No previous token found, creating a new one")
                        engine.JWT_action(username, access_token, get_csrf_token(access_token), ACCESS_EXPIRES.total_seconds(), "add")
                        print(currentLine("app", "LOGIN"), "JWT Token added")
                    else:
                        ### CHECK IF THE JWT TOKEN IS ALREADY IN THE DATABASE AND ADD JWT CODE + CSRF TOKEN TO THE DATABASE
                        if(engine.JWT_action(username, used_token, get_csrf_token(used_token), ACCESS_EXPIRES.total_seconds(), "check")):
                            engine.JWT_action(username, access_token, get_csrf_token(access_token), ACCESS_EXPIRES.total_seconds(), "update")
                            print(currentLine("app", "LOGIN"), "JWT Token updated")
                        # else:
                        #     engine.JWT_action(username, access_token, get_csrf_token(access_token), ACCESS_EXPIRES.total_seconds(), "add")
                        #     print(currentLine("app", "LOGIN"), "JWT Token added")

                    print(currentLine("app", "LOGIN"), "User logged in successfully")    
                    return resp
                else: return jsonify({"code": 401, "message": "This user does not exist"}), 200
            else:
                print(currentLine("app", "LOGIN", "ERROR"), "Failed request")
                return jsonify({"code": 401, "message": "Login failed"}), 200
        except Exception as error:
            print(currentLine("app", "LOGIN", "ERROR"), error)
            return jsonify({"code": 401, "message": "Login failed"}), 200
    else:
        print(currentLine("app", "LOGIN", "ERROR"), "It is not a json media type")
        return jsonify({"code": 401, "message": "Login failed"}), 200
            
            
### LOADS REGISTER PAGE --- METHOD = 'GET'
@app.route("/register", methods=['GET'])
def registerPage():
    return render_template("register.html")
    
    
 ### SUBSCRIBE NEW USER TO DB --- METHOD = 'POST'
@app.route("/register", methods=['POST'])
def register():
    print(currentLine("app", "REGISTER"), " I\'m inside subscribe function")
    if (request.is_json):
        try:
            if(request.get_json() != None):
                username = request.get_json()['username']
                password = request.get_json()['password']
                if engine.account(True, username, password=password):
                    print(currentLine("app", "REGISTER"), "User created")
                    access_token = create_access_token(identity=username, expires_delta=ACCESS_EXPIRES)
                    print(currentLine("app", "REGISTER"), "Token created")
                    tmp_access = jsonify(access_token=access_token, message="Registration success!", code=200)
                    set_access_cookies(response=tmp_access, encoded_access_token=access_token)
                    ### ADD JWT CODE + CSRF TOKEN TO THE DATABASE
                    if(engine.JWT_action(username, access_token, get_csrf_token(access_token), ACCESS_EXPIRES.total_seconds(), "add")):
                        return tmp_access
                    else:
                        return jsonify(message="Registration success!", code= 400), 200
                else:
                    print(currentLine("app", "REGISTER", "ERROR"), "Register failed")
                    return jsonify(message="Registration failed", code=400), 400
            else:
                print(currentLine("app", "REGISTER", "ERROR"), "Failed request")
                return render_template("register.html", check=False), 400
        except Exception as error:
            print(currentLine("app", "REGISTER", "ERROR"), error)
            return render_template("error.html", error=error)
    else:
        print(currentLine("app", "REGISTER", "ERROR"), "It is not a json media type")
        return render_template("register.html", check=False)
       
       
### LOADS LOGOUT PAGE --- METHOD = 'GET'
@app.route("/logout", methods=['GET'])
@jwt_required()
def logoutPage():
    engine.JWT_action(get_jwt()['sub'], get_jwt(), get_jwt()['csrf'], ACCESS_EXPIRES.total_seconds(), "revoke")
    response = make_response(render_template("logout.html/"),get_jwt())
    unset_jwt_cookies(response=response)
    print(currentLine("app", "LOGOUT"), "User logged out successfully")
    return response, 302


### LOADS DOWNLOAD CERTIFICATE PAGE --- METHOD = 'GET'
@app.route("/downloadcertificate", methods=['GET'])
def downloadCertificatePage():
    return render_template("download.html")


### HANDLE OF STATUS CODE OF ERROR (400 AND 500)
@app.errorhandler(werkzeug.exceptions.NotFound)
def not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Error'] = 'A value'
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
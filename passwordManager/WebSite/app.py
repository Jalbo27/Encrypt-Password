import string, random, werkzeug.exceptions, time
from datetime import datetime, timedelta, timezone
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

ACCESS_EXPIRES=timedelta(minutes=1)

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
    PERMANENT_SESSION_LIFETIME=ACCESS_EXPIRES
)

jwt = JWTManager(app)

engine = Engine()
password_dict = []

### REFRESH JWT TOKENS
@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp >= exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
            return response
        else:
            return redirect(url_for("login"))
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    return redirect(url_for("login", alert="You have been logged out because the session is terminated"), code=307)

### LOADS HOMEPAGE WINDOW --- METHOD = 'GET'
@app.route("/")
@app.route("/homepage/", methods=['GET'])
def homepage_Page():
    return render_template("homepage.html")


### LOADS HOMEPAGE WINDOW WITH AN AUTHENTICATED ACCOUNT --- METHOD = 'GET' 
@app.route("/homepage/<string:account>", methods=['GET'])
@jwt_required()
def home_page(account=''):
    print(currentLine("app"), request.headers)
    if account != '':
        try:
            current_user = get_jwt_identity()
            print(currentLine("app"), current_user)
            print(currentLine("app"), "Il codice JWT dell'utente è: ",request.cookies.get('access_token_cookie'))
            if current_user == account and engine.checkJWT(request.cookies.get('access_token_cookie')):
                print(currentLine("app"), "gli utenti combaciano")
                if(password_dict != []):
                    return render_template("homepage.html", account=escape(account), passwords=engine.getAllPasswords(account))
                else:
                    return render_template("homepage.html", account=escape(account))
            else:
                print(currentLine("app"), "gli utenti non combaciano")
                return redirect(url_for("login"))
        except Exception as e:
            print(currentLine("app"), e)
            return redirect(url_for("login"))


### UPLOAD THE PASSWORD INTO TABLE --- METHOD = 'POST'
@app.route("/homepage/", methods=['POST'])
@app.route("/homepage/<string:account>", methods=['POST'])
@jwt_required()
def uploadPassword(account=''):
    if(request.is_json):
        print(currentLine("app"), "JSON received and is valid")
        if(account == ''):
            return jsonify({"message": "You have not an account. You have to login before", "code": 401}), 200
        response = None
        if (account == get_jwt_identity()):
            ### CHECK THE ACTION: 'submit', 'delete', 'edit'
            if(request.get_json()['action'] == 'submit'):
                password_dict.append(request.get_json())
                if (engine.sanityPassword(password_dict[-1])):
                    print(currentLine("app"),"I\'m here password sanity check passed successfully")
                    password_dict[-1]['id'] += 1
                    del password_dict[-1]['action']
                    if (engine.addPassword(account, password_dict[-1])):
                        print(password_dict[-1])
                        del password_dict[-1]['_id']
                        response = jsonify({"id": password_dict[-1]['id'], "message": "Password added successfully", "code": 200})
                    else:
                        response = jsonify({"message": "failed to load password or there are problems in some fields", "code": 4117})
                else:
                    response = jsonify({"message": "failed to load password or there are problems in some fields", "code": 4117})
                return response, 200
                
            ### DELETE: Delete password of the current account
            elif (request.get_json()['action'] == 'delete'):
                if engine.deletePassword(account, int(request.get_json()['id'])):
                    print(currentLine("app"), "password deleted")
                    response = jsonify({"message": "Password deleted successfully", "code": 200})
                else:
                    print(currentLine("app"), "Password was not delete")
                    response = jsonify({"message": "Error to delete the password", "code": 417})
                return response, 200
            ### EDIT: Edit a password of the current account
            elif (request.get_json()['action'] == 'edit'):
                if engine.deletePassword(account, int(request.get_json()['id'])):
                    response = jsonify({"message": "Password modified successfully", "code": 200})
                else:
                    response = jsonify({"message": "Error to modify the password", "code": 417})
                return response, 200
            ### Wrong request
            else:
                print(currentLine("app"), request.headers, "\n")
                print(currentLine("app"), "Bad request")
                return render_template("homepage.html")
        else:
            return jsonify({"message": "You have not an account. You have to login before", "code": 401}), 200
    ### The request sent is not json media type
    else:
        print(currentLine("app"), request.headers, "\n")
        print(currentLine("app"), "It is not a json media type")
        return render_template("homepage.html")
    
    
### LOADS LOGIN PAGE --- METHOD = 'GET'
@app.route("/login", methods=['GET'])
def loginPage(alert=''):
    print(currentLine("app"),"I\'m inside loginPage function")    
    if alert != '': return render_template("login.html", alert=alert)
    else: return render_template("login.html")


### CREATE OR LOGIN AN ACCOUNT --- METHOD = 'POST'
@app.route("/login", methods=['POST'])
def login():
    print(currentLine("app"), " I\'m logging an account")
    if (request.is_json):
        print(currentLine("app"), request.get_json())
        try:
            if(request.get_json() != None):
                username = request.get_json()['username']
                password = request.get_json()['password']
                if engine.account(username, password, False):
                    access_token = create_access_token(identity=username, fresh=timedelta(minutes=1))
                    resp = jsonify({"access_token": access_token, "message": "login success", "code": 200})
                    set_access_cookies(response=resp, encoded_access_token=access_token)
                    ### ADD JWT CODE + CSRF TOKEN TO THE DATABASE
                    if(engine.JWT_action(username, access_token, get_csrf_token(access_token), ACCESS_EXPIRES.total_seconds(), "add")):
                        print(currentLine("app"), "Utente loggato correttamente")
                        return resp
                    else:
                        print(currentLine("app"), "Login failed")
                        return jsonify({"code": 401, "message": "Bad username or password"}), 200
                else: return jsonify({"code": 401, "message": "This user does not exist"}), 200
            else:
                print(currentLine("app"), "Failed request")
                return jsonify({"code": 401, "message": "Login failed"}), 200
        except Exception as error:
            print(currentLine("app"), error)
            return jsonify({"code": 401, "message": "Login failed"}), 200
    else:
        print(currentLine("app"), " It is not a json media type")
        return jsonify({"code": 401, "message": "Login failed"}), 200
            
            
### LOADS REGISTER PAGE --- METHOD = 'GET'
@app.route("/register", methods=['GET'])
def registerPage():
    return render_template("register.html")
    
    
 ### SUBSCRIBE NEW USER TO DB --- METHOD = 'POST'
@app.route("/register", methods=['POST'])
def register():
    print(currentLine("app"), " I\'m inside subscribe function")
    if (request.is_json):
        try:
            if(request.get_json() != None):
                username = request.get_json()['username']
                password = request.get_json()['password']
                if engine.account(username, password, True):
                    print(currentLine("app"), " User created")
                    access_token = create_access_token(identity=username, fresh=timedelta(minutes=1))
                    tmp_access = jsonify({"access_token": access_token, "message": "Registration success!", "code": 200})
                    set_access_cookies(response=tmp_access, encoded_access_token=access_token)
                    ### ADD JWT CODE + CSRF TOKEN TO THE DATABASE
                    if(engine.JWT_action(username, access_token, get_csrf_token(access_token), ACCESS_EXPIRES.total_seconds(), "add")):
                        return tmp_access
                    else:
                        return jsonify({"message": "Registration success!", "code": 417}), 200
                else:
                    print(currentLine("app"), " Register failed")
                    return jsonify(message="Registration failed", code=417), 417
            else:
                print(currentLine("app"), " Failed request")
                return render_template("register.html", check=False), 200
        except Exception as error:
            print(currentLine("app"), error)
            return render_template("error.html", error=error)
    else:
        print(currentLine("app"), " It is not a json media type")
        return render_template("register.html", check=False)
       
       
### LOADS LOGOUT PAGE --- METHOD = 'GET'
@app.route("/logout", methods=['GET'])
@jwt_required()
def logoutPage():
    engine.JWT_action(get_jwt()['sub'], get_jwt(), get_jwt()['csrf'], ACCESS_EXPIRES.total_seconds(), "revoke")
    response = make_response(render_template("logout.html/"),get_jwt())
    unset_jwt_cookies(response=response)
    print(currentLine("app"), response.headers)
    return response, 302


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
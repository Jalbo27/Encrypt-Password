from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from engine import Engine
from markupsafe import escape
from __inspection__ import currentLine

app = Flask(__name__)

responder = Engine()
password_dict = []

### LOADS HOMEPAGE PAGE --- METHOD = 'GET'
@app.route("/")
@app.route("/homepage/")
@app.route("/homepage/<string:account>", methods=['GET'])
def home_page(account=''):
    return render_template("homepage.html", account=escape(account), id=len(password_dict)) 

### UPLOAD THE PASSWORD INTO TABLE
@app.route("/homepage/", methods=['POST'])
@app.route("/homepage/<string:account>", methods=['POST'])
def uploadPassword(account=''):
    if(request.is_json):
        print(currentLine("app"), request.headers)
        if(account == ''):
            return jsonify({'message': 'You have not an account. You have to login before', 'status': 'failed'})
        
        password_dict.append(request.get_json())
        print(currentLine("app"), password_dict)
        name = password_dict[-1]['name']
        username = password_dict[-1]['username']
        password = password_dict[-1]['password']
        uri = password_dict[-1]['uri']
        if (responder.sanityPassword(name, username, password, uri)):
            print(currentLine("app")," I\'m here password sanity check passed successfully")
            if(responder.addPassword(account, password_dict[-1])):
                print(currentLine("app"), 'password added')
                print(currentLine("app"), 'response sent')
                password_dict[-1]['id'] += 1
                password_dict[-1]['status'] = 'Ok'
                return jsonify(password_dict[-1])
            else:
                return jsonify({'message': 'failed to load password or there are problems in some fields', 'status': 'failed'})
        else:
            return jsonify({'message': 'failed to load password or there are problems in some fields', 'status': 'failed'})
    else:
        print(currentLine("app"), request.headers, "\n")
        print(currentLine("app"), " It is not a json media type")
        return jsonify(request)
    
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
                if responder.account(username, password, True):
                    print(currentLine("app"), " User created")
                    return jsonify({"code": 200, "url": f"/homepage/"})
                    #return redirect(url_for(home_page, name=username), code=302)
                else:
                    print(currentLine("app"), " Login failed")
                    response = {'login': 'failed'}
                    return jsonify(response)
            else:
                print(currentLine("app"), " Failed request")
                return render_template("login.html", check=False)
        except Exception as error:
            print(currentLine("app"), error)
            return render_template("login.html", check=False)
    else:
        print(currentLine("app"), " It is not a json media type")
        return render_template("login.html", check=False)
            
### LOADS REFGISTER PAGE --- METHOD = 'GET'
@app.route("/register", methods=['GET'])
def registerPage():
    return render_template("register.html")
    
 ###
@app.route("/register", methods=['POST'])
def register():
    pass
       
### LOADS LOGOUT PAGE --- METHOD = 'GET'
@app.route("/logout")
def logoutPage():
    return render_template("logout.html/")

### HANDLE OF STATUS CODE OF ERROR (400 AND 500)
@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from engine import Engine
from markupsafe import escape

app = Flask(__name__)

responder = Engine()
password_dict = []

### 
@app.route("/")
@app.route("/homepage/")
@app.route("/homepage/<string:name>")
def home_page(name=''):
    return render_template("homepage.html", account=escape(name), id=len(password_dict)) 

### Upload the password 
@app.route("/homepage/<string:name>", methods=['POST'])
def uploadPassword(name=''):
    if(request.is_json):
        password_dict.append(request.get_json())
        print('i\'m here', password_dict)
        name = password_dict[-1]['name']
        username = password_dict[-1]['username']
        password = password_dict[-1]['password']
        uri = password_dict[-1]['uri']
        if (responder.sanityPassword(name, username, password, uri)):
            print('i\'m here inside sanity password function')
            responder.addPassword(name, password_dict)
            print('response sent')
            password_dict[-1]['id'] += 1
            return jsonify(password_dict[-1])
        else:
            return render_template("homepage.html/")
    else:
        print(request.headers)
        print("It is not a json media type")
        return jsonify(request)
    
### LOADS LOGIN PAGE --- METHOD = 'GET'
@app.route("/login", methods=['GET'])
def loginPage():
    print("I\'m inside loginPage function")    
    return render_template("login.html") 

### CREATE OR LOGIN AN ACCOUNT --- METHOD = 'POST'
@app.route("/login", methods=['POST'])
def login():
    print("I\'m inside login function")
    if (request.is_json):
        print(request.get_json())
        try:
            if(request.get_json() != None):
                username = request.get_json()['username']
                password = request.get_json()['password']
                if responder.account(username, password, True):
                    print("User created")
                    return jsonify({"code": 200, "url": f"/homepage/"})
                    #return redirect(url_for(home_page, name=username), code=302)
                else:
                    print("Login failed")
                    response = {'login': 'failed'}
                    return jsonify(response)
            else:
                print("Failed request")
                return render_template("login.html", check=False)
        except Exception as error:
            print(error)
            return render_template("login.html", check=False)
    else:
        print("It is not a json media type")
        return render_template("login.html", check=False)
            
###
@app.route("/register")
def register():
    pass
    
###
@app.route("/logout")
def logoutPage():
    return render_template("logout.html/")

###
@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp
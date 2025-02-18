from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from engine import Engine
from markupsafe import escape

app = Flask(__name__)

responder = Engine()
password_dict = []

### 
@app.route("/")
@app.route("/homepage/")
@app.route("/homepage/<string:account>", methods=['GET'])
def home_page(account=''):
    return render_template("homepage.html", account=escape(account), id=len(password_dict)) 

### Upload the password 
@app.route("/homepage/", methods=['POST'])
@app.route("/homepage/<string:account>", methods=['POST'])
def uploadPassword(account=''):
    if(request.is_json):
        print("[app.py] 22: headers: ", request.headers)
        if(account == ''):
            return jsonify({'message': 'You have not an account. You have to login before', 'status': 'failed'})
        
        password_dict.append(request.get_json())
        print('[app.py] 27: i\'m here', password_dict)
        name = password_dict[-1]['name']
        username = password_dict[-1]['username']
        password = password_dict[-1]['password']
        uri = password_dict[-1]['uri']
        if (responder.sanityPassword(name, username, password, uri)):
            print('[app.py] 33: i\'m here password sanity check passed successfully')
            responder.addPassword(account, password_dict[-1])
            print('[app.py] 35: response sent')
            password_dict[-1]['id'] += 1
            password_dict[-1]['status'] = 'Ok'
            return jsonify(password_dict[-1])
        else:
            return jsonify({'message': 'failed to load password or there are problems in some fields', 'status': 'failed'})
    else:
        print("[app.py] 42:", request.headers, "\n")
        print("[app.py] 43: It is not a json media type")
        return jsonify(request)
    
### LOADS LOGIN PAGE --- METHOD = 'GET'
@app.route("/login", methods=['GET'])
def loginPage():
    print("[app.py] 49: I\'m inside loginPage function")    
    return render_template("login.html") 

### CREATE OR LOGIN AN ACCOUNT --- METHOD = 'POST'
@app.route("/login", methods=['POST'])
def login():
    print("[app.py] 55: I\'m inside login function")
    if (request.is_json):
        print("[app.py] 57: ", request.get_json())
        try:
            if(request.get_json() != None):
                username = request.get_json()['username']
                password = request.get_json()['password']
                if responder.account(username, password, True):
                    print("[app.py] - line 63: User created")
                    return jsonify({"code": 200, "url": f"/homepage/"})
                    #return redirect(url_for(home_page, name=username), code=302)
                else:
                    print("[app.py] 67: Login failed")
                    response = {'login': 'failed'}
                    return jsonify(response)
            else:
                print("[app.py] 71: Failed request")
                return render_template("login.html", check=False)
        except Exception as error:
            print("[app.py] 74: ", error)
            return render_template("login.html", check=False)
    else:
        print("[app.py] 77: It is not a json media type")
        return render_template("login.html", check=False)
            
###
@app.route("/register", methods=['GET'])
def registerPage():
    return render_template("register.html")
    
 ###
@app.route("/register", methods=['POST'])
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
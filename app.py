import json
import jwt
from bson import json_util
from flask import Flask, request, session, jsonify
import bcrypt
from dbConnect import records

app = Flask(__name__)
app.secret_key = "thisissecretkey"


@app.route("/register", methods=['POST', 'get'])
def register():
    message = ''
    if "email" in session:
        message = 'you are already logged in'
        return jsonify(message=message, status_code=200)
    if request.method == "POST":
        getdata = request.get_json()
        user = getdata['user']
        email = getdata['email']
        password1 = getdata['password1']
        password2 = getdata['password2']
        user_found = records.find_one({"name": user})
        email_found = records.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that name'
            return jsonify(message=message, data=getdata, status_code=200)
        if email_found:
            message = 'This email already exists in database'
            return jsonify(message=message, data=getdata, status_code=200)
        if password1 != password2:
            message = 'Passwords should match!'
            return jsonify(message=message, data=getdata, status_code=200)

        else:
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            user_input = {'name': user, 'email': email, 'password': hashed}
            records.insert_one(user_input)
            message = email + ' user created ' + "Hello: " + user
            return jsonify(message=message, data=getdata, status_code=200)
    message = 'Try again'
    return jsonify(message=message)


@app.route('/logged_in')
def logged_in():
    if "email" in session:
        email = session["email"]
        message = "You are already logged in session"
        return jsonify(message=message, email=email)

    else:
        message = 'you are logged out'
        return jsonify(message=message, status_code=200)


@app.route("/login", methods=["POST", "GET"])
def login():
    message = 'Please login to your account'
    if "email" in session:
        message = 'already logged in'
        return jsonify(message=message, email=session, status_code=200)

    if request.method == "POST":
        getdata = request.get_json()
        email = getdata["email"]
        password = getdata["password"]

        email_found = records.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']

            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                message = 'right password'
                return jsonify(message=message, status_code=200)
            else:
                if "email" in session:
                    return jsonify(message=message, status_code=200)
                message = 'Wrong password'
                return jsonify(message=message, status_code=200)
        else:
            message = 'Email not found'
            return jsonify(message=message, status_code=200)
    return jsonify(message=message, status_code=200)


@app.route("/logout", methods=["POST", "GET"])
def logout():
    message = ' to your account'
    if "email" in session:
        session.pop("email", None)
        message = 'account'
        return jsonify(message=message, status_code=200)
    else:

        return jsonify(message=message, status_code=200)


@app.route("/")
def getinfo():
    postdata = {
        "user": "sample_user",
        "email": "sample@abc.com",
        "password1": "123456789**",  # it should be 8 digits with special charater
        "password2": "123456789**"
    }
    message = 'You will get this message with status code and data'
    return jsonify(message=message, data=postdata, status_code=200)


@app.route("/dashboard/<user>")
def dashboard(user):
    # getprofile = request.get_json()
    if "email" in session:
        semail = session['email']
        email_found = records.find_one({"email": semail})
        message = 'user found'
        data = json.loads(json_util.dumps(email_found))
        return jsonify(message=message, data=data, status_code=200)
    else:
        message = 'USER NOT FOUND'
        return jsonify(message=message, status_code=404)


# end of code to run it
if __name__ == "__main__":
    app.run(debug=True)

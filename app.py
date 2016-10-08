from flask import Flask, request, jsonify, session
from functools import wraps
from json import loads as jason

app = Flask(__name__)

@app.route("/auth/", methods=["GET", "POST"])
def auth():
    """
    Simple GET/POST authentication method. Send POST with JSON with 'auth-token'
    key to auth, send GET request to de-auth
    """
    if request.method == "POST":
        data = jason(request.data)
        session['auth-token'] = data['auth-token']
        session['speed'] = 'UNSET'
    else:
        session.clear()

@app.route("/speed/", methods=["GET", "POST"])
def setspeed():
    """
    Sets the current speed provided as JSON
    """
    success = { 'status' : 'ok' }
    authfail = { 'status' : 'invalid auth' }
    errmsg = { 'status' : 'error' }
    if request.method == "POST":
        try:
            data = jason(request.data)
            if "auth-token" in session and session["auth-token"] == data["auth-token"]:
                session["speed"] = data["speed"]
                return jsonify(**success)
            else:
                return jsonify(**authfail)
        except:
            return jsonify(**errmsg)
    else:
        try:
            if "auth-token" in session and session["auth-token"] == data["auth-token"]:
                d = { 'status' : 'ok', 'speed' : session['speed'] }
                return jsonify(**d)
            else:
                return jsonify(**authfail)
        except:
            return jsonify(**errmsg)

if __name__ == "__main__":
    app.debug = True
    app.run('0.0.0.0', port=11235)


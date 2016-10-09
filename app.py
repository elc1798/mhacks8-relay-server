from flask import Flask, request, jsonify
from functools import wraps
from json import loads as jason

app = Flask(__name__)

DATA = {}

@app.route("/auth/", methods=["GET", "POST"])
def auth():
    """
    Simple GET/POST authentication method. Send POST with JSON with 'auth-token'
    key to auth, send GET request to de-auth
    """
    global DATA
    success = { 'status' : 'ok' }
    errmsg = { 'status' : 'error' }
    if request.method == "POST":
        data = jason(request.data)
        DATA['speed'] = 'UNSET'
        return jsonify(**success)
    else:
        if "soeed" in DATA:
            DATA = {}
            return jsonify(**success)
        else:
            return jsonify(**errmsg)

@app.route("/speed/", methods=["GET", "POST"])
def setspeed():
    """
    Sets the current speed provided as JSON
    """
    global DATA
    success = { 'status' : 'ok' }
    errmsg = { 'status' : 'error' }
    if request.method == "POST":
        try:
            data = jason(request.data)
            DATA["speed"] = data["speed"]
            DATA["accel"] = data["accel"]
            return jsonify(**success)
        except:
            return jsonify(**errmsg)
    else:
        try:
            d = { 'status' : 'ok', 'speed' : DATA['speed'], 'accel' : DATA['accel'] }
            return jsonify(**d)
        except:
            return jsonify(**errmsg)

@app.route("/temp")
@app.route("/temp/")
def temp_endpoint():
    d = { 'status' : 'ok', 'speed' : 123.456 }
    return jsonify(**d)

if __name__ == "__main__":
    app.debug = True
    app.secret_key = "janky-relay-server"
    app.run('0.0.0.0', port=11235)


#!/usr/bin/env python

import datetime as dt
import os
import sys

from flask import Flask
from flask import request
from flask.json import jsonify

app = Flask(__name__)

@app.route("/cdc-event", methods=["POST"])
def log_event():
    payload = request.get_json()

    print(payload)

    return jsonify({}), 200

@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    return jsonify({"healthy" : True}), 200
    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8000")

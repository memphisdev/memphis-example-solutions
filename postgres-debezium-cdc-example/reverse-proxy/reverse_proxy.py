#!/usr/bin/env python

import datetime as dt
import logging
import os
import sys

from flask import Flask
from flask import request
from flask.json import jsonify

app = Flask(__name__)

import datetime as dt
import json
import requests
import time

MEMPHIS_HOST_KEY = "MEMPHIS_HOST"
MEMPHIS_PORT_KEY = "MEMPHIS_PORT"
MEMPHIS_USERNAME_KEY = "MEMPHIS_USERNAME"
MEMPHIS_PASSWORD_KEY = "MEMPHIS_PASSWORD"

DEFAULT_PORT = "4444"

EXPIRATION_MIN = 3600
REFRESH_EXPIRATION_MIN = 10000092

logging.basicConfig(level=logging.INFO)

refresh_token = None
jwt_token = None

def authenticate():
    global jwt_token
    global refresh_token

    refresh = refresh_token != None    

    payload = {
      "token_expiry_in_minutes": EXPIRATION_MIN,
      "refresh_token_expiry_in_minutes": REFRESH_EXPIRATION_MIN
    }

    if refresh:
        host = os.environ[MEMPHIS_HOST_KEY]
        port = os.environ.get(MEMPHIS_PORT_KEY, DEFAULT_PORT)
        url = "http://{}:{}/auth/refreshToken".format(host, port)

        logging.info("Trying to refresh authorization")
        payload.update({
            "jwt_refresh_token": refresh_token
        })
    else:
        host = os.environ[MEMPHIS_HOST_KEY]
        port = os.environ.get(MEMPHIS_PORT_KEY, DEFAULT_PORT)
        url = "http://{}:{}/auth/authenticate".format(host, port)

        logging.info("Trying initial authorization")
        payload.update({
              "username": os.environ[MEMPHIS_USERNAME_KEY],
              "password": os.environ[MEMPHIS_PASSWORD_KEY],

        })

    headers = {
      "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        logging.error("Authentication failure")
        logging.error("Status code: {}".format(response.status_code))
        logging.error("Response: {}".format(response.text))
        return False

    logging.info("Authentication success")

    response_payload = response.json()
    jwt_token = response_payload["jwt"]
    refresh_token = response_payload["jwt_refresh_token"]

    return True

def forward_to_memphis(station, payload):
    host = os.environ[MEMPHIS_HOST_KEY]
    port = os.environ.get(MEMPHIS_PORT_KEY, DEFAULT_PORT)

    url = "http://{}:{}/stations/{}/produce/single".format(host, port, station)

    headers = {
        "Authorization": "Bearer {}".format(jwt_token),
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, data=payload)

    # need to reauthenticate
    if response.status_code == 401:
        logging.info("Need to reauthorize")
        auth_success = authenticate()
        if not auth_success:
            return jsonify({}), 500
        
        headers = {
            "Authorization": "Bearer {}".format(jwt_token),
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, data=payload)    

    if response.status_code >= 300:
        logging.warning("Failed to forward payload to {}".format(url))
        logging.warning("Status code: {}".format(response.status_code))
        logging.warning("Memphis response: {}".format(response.text))
        return False

    logging.info("Successfully forward message to Memphis")

    return True

@app.route("/cdc-event/<station>", methods=["POST"])
def log_event(station):
    auth_success = authenticate()

    if not auth_success:
        return jsonify({}), 500

    payload = request.get_data()
    forward_success = forward_to_memphis(station, payload)

    if not forward_success:
        return jsonify({}), 500
    
    return jsonify({}), 200
    
if __name__ == "__main__":
    for key in [MEMPHIS_HOST_KEY, MEMPHIS_USERNAME_KEY, MEMPHIS_PASSWORD_KEY]:
        if key not in os.environ:
            logging.error("Expected environmental variable {} not set".format(key))
            sys.exit(1)

    app.run(debug=True, host="0.0.0.0", port="8000")

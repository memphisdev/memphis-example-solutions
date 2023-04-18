import datetime as dt
import json
import logging
import requests
import time

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    url = "http://localhost:8000/cdc-event/todo-cdc-events"

    keep_going = True
    while keep_going:
        time.sleep(0.5)
        
        payload = {
            "message": "New Message",
            "timestamp" : dt.datetime.now().isoformat()
        }

        response = requests.post(url, json=payload)

        logging.info("Test message sent. Response status code: {}".format(response.status_code))

        if response.status_code not in [200, 201]:
           keep_going = False

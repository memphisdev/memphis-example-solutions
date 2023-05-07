#!/usr/bin/env python

import datetime as dt
import os
import random
import time
import sys

from pymongo import MongoClient

HOST_KEY = "MONGO_HOST"
USER_PASSWORD_KEY = "MONGO_PASSWORD"
USER_USERNAME_KEY = "MONGO_USERNAME"

PORT_KEY = "MONGO_PORT"
DEFAULT_PORT = 27017

DATABASE_NAME = "todo_application"
COLLECTION_NAME = "todo_items"

DESCRIPTION_LENGTH = 20
ASCII_START = 65 # uppercase A
ASCII_END = 90 # uppercase Z

if __name__ == "__main__":
    for key in [HOST_KEY, USER_USERNAME_KEY, USER_PASSWORD_KEY]:
        if key not in os.environ:
            msg = "Must specify environmental variable {}".format(key)
            print(msg)
            sys.exit(1)

    db_uri = "mongodb://{}:{}@{}:{}/".format(os.environ.get(USER_USERNAME_KEY),
                                             os.environ.get(USER_PASSWORD_KEY),
                                             os.environ.get(HOST_KEY),
                                             os.environ.get(PORT_KEY, DEFAULT_PORT))

    client = MongoClient(db_uri)
    db = client[DATABASE_NAME]

    if COLLECTION_NAME in db.list_collection_names():
        db.drop_collection(COLLECTION_NAME)

    # using this syntax to enable pre- and post-images
    # these are needed to populate the "before" fields
    # for CDC
    collection = db.create_collection(name=COLLECTION_NAME,
                                      changeStreamPreAndPostImages={ "enabled" : True })

    while True:
        todo_item = {}
    
        # generate a todo item
        creation_timestamp = dt.datetime.now()
        todo_item["creation_timestamp"] = creation_timestamp        
        todo_item["due_date"] = None if random.random() >= 0.5 else creation_timestamp + dt.timedelta(days=3)

        chars = [chr(random.randint(ASCII_START, ASCII_END)) 
                    for i in range(DESCRIPTION_LENGTH)]
        todo_item["description"] = "".join(chars)

        todo_item["completed"] = random.random() < 0.1

        collection.insert_one(todo_item)
        print(todo_item)

        # 0.5 sec delay between items
        time.sleep(0.5)

    # this will probably never be reached
    # because we're not trapping signals
    client.close()

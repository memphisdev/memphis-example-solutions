from __future__ import annotations
import asyncio
import datetime as dt
import json
import logging
import os
import random
import sys
import time

from memphis import Memphis, Headers, MemphisError, MemphisConnectError, MemphisHeaderError, MemphisSchemaError

STATION_KEY = "MEMPHIS_STATION"
USERNAME_KEY = "MEMPHIS_USERNAME"
PASSWORD_KEY = "MEMPHIS_PASSWORD"
HOST_KEY = "MEMPHIS_HOST"

DESCRIPTION_LENGTH = 20
ASCII_START = 65 # uppercase A
ASCII_END = 90 # uppercase Z

def generate_todo_items():
    while True:
        todo_item = {}
    
        # generate a todo item
        creation_timestamp = dt.datetime.now()
        due_date = int((creation_timestamp + dt.timedelta(days=3)).timestamp())
        description = "".join([chr(random.randint(ASCII_START, ASCII_END))
                               for i in range(DESCRIPTION_LENGTH)])
        completed = random.random() < 0.1

        todo_item["_id"] = { "$oid" : "abc25" }
        todo_item["creation_timestamp"] = { "$date" : int(creation_timestamp.timestamp()) }
        todo_item["due_date"] = None if random.random() >= 0.5 else { "$date" : due_date }
        todo_item["description"] = description
        todo_item["completed"] = completed
    
        # 25% of messages will be "bad"
        if random.random() < 0.25:
            r = random.random()
            key = random.choice(list(todo_item.keys()))
            if r < 0.3333: # drop required key
                del todo_item[key]
            elif r < 0.6666: # assign value of wrong type to key
                todo_item[key] = -5000
            else: # set item to null
                todo_item[key] = None

        yield todo_item

async def main():
    try:
        item_generator = generate_todo_items()
        
        memphis = Memphis()
        await memphis.connect(host=os.environ[HOST_KEY], username=os.environ[USERNAME_KEY], password=os.environ[PASSWORD_KEY])

        producer = await memphis.producer(station_name=os.environ[STATION_KEY], producer_name="test-producer")
        
        for item in item_generator:
            print(item)
            msg = json.dumps(item)
            print("Sending message: {}".format(msg))
            try:
                await producer.produce(bytearray(msg, "utf-8"))
            # The message is still sent even if a schema error occurs
            # we want to supress the error because we'll handle schema
            # violations in another place
            except MemphisSchemaError as e:
                print(e)
                print("Continuing...")
            time.sleep(0.5)

    except (MemphisError, MemphisConnectError, MemphisHeaderError) as e:
        print(type(e))
        print(e)

    finally:
        await memphis.close()

if __name__ == "__main__":
    for key in [HOST_KEY, USERNAME_KEY, PASSWORD_KEY, STATION_KEY]:
        if key not in os.environ:
            logging.error("Expected environmental variable {} not set".format(key))
            sys.exit(1)

    asyncio.run(main())

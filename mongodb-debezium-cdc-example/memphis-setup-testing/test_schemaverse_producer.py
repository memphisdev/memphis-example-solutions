from __future__ import annotations
import asyncio
import datetime as dt
import json
import os
import pprint
import random
import sys
import time

from memphis import Memphis, Headers, MemphisError, MemphisConnectError, MemphisHeaderError, MemphisSchemaError

STATION_KEY = "MEMPHIS_STATION"
USERNAME_KEY = "MEMPHIS_USERNAME"
PASSWORD_KEY = "MEMPHIS_PASSWORD"
HOST_KEY = "MEMPHIS_HOST"
DELAY_KEY = "DELAY_SEC"

DESCRIPTION_LENGTH = 20
ASCII_START = 65 # uppercase A
ASCII_END = 90 # uppercase Z

def simulated_cdc_events():
    while True:
        # generate a todo item
        todo_item = {}
        creation_timestamp = dt.datetime.now()
        todo_item["_id"] = { "$oid" : "abcdefabcdef" }
        todo_item["creation_timestamp"] = { "$date" : 123 }
        todo_item["due_date"] = None if random.random() >= 0.5 else { "$date" : 123 }
        chars = [chr(random.randint(ASCII_START, ASCII_END))
                    for i in range(DESCRIPTION_LENGTH)]
        todo_item["description"] = "".join(chars)
        todo_item["completed"] = random.random() < 0.1

        # break the schema by deleting a key or changing to an unexpected type
        if random.random() < 0.25:
            key = random.choice(list(todo_item.keys()))
            if random.random() < 0.5:
                del todo_item[key]
            else:
                todo_item[key] = -5000

        cdc_event = {
            "schema" : None,
            "payload" : {
                "before" : todo_item,
                "after" : None
            }
        }

        yield cdc_event

async def main(host, username, password, station, delay_sec):
    try:
        memphis = Memphis()
        await memphis.connect(host=host, username=username, password=password)

        producer = await memphis.producer(station_name=station, producer_name="test-producer")

        for msg in simulated_cdc_events():
            pprint.pprint(msg)
            output_str = json.dumps(msg)
            output_bytes = bytearray(output_str, "utf-8")

            await producer.produce(message=output_bytes)
            
            time.sleep(delay_sec)
            print()

    except (MemphisError, MemphisConnectError, MemphisHeaderError, MemphisSchemaError) as e:
        print(e)

    finally:
        await memphis.close()

if __name__ == "__main__":
    for key in [HOST_KEY, USERNAME_KEY, PASSWORD_KEY, STATION_KEY, DELAY_KEY]:
        if key not in os.environ:
            logging.error("Expected environmental variable {} not set".format(key))
            sys.exit(1)

    asyncio.run(main(os.environ.get(HOST_KEY),
                     os.environ.get(USERNAME_KEY),
                     os.environ.get(PASSWORD_KEY),
                     os.environ.get(STATION_KEY),
                     float(os.environ.get(DELAY_KEY))))

from __future__ import annotations
import asyncio
import json
import logging
import os
import sys
import time

from memphis import Memphis, Headers, MemphisError, MemphisConnectError, MemphisHeaderError, MemphisSchemaError

STATION_KEY = "MEMPHIS_STATION"
USERNAME_KEY = "MEMPHIS_USERNAME"
PASSWORD_KEY = "MEMPHIS_PASSWORD"
HOST_KEY = "MEMPHIS_HOST"

async def main():
    try:
        memphis = Memphis()
        await memphis.connect(host=os.environ[HOST_KEY], username=os.environ[USERNAME_KEY], password=os.environ[PASSWORD_KEY])

        producer = await memphis.producer(station_name=os.environ[STATION_KEY], producer_name="test-producer")
        msg_obj = { "schema" : None,
                    "payload" : { "before" : "{\"key\" : 123}",
                                  "after" : "{\"key\" : 456}" }
                  }
        while True:
            msg = json.dumps(msg_obj)
            print("Sending message: {}".format(msg))
            await producer.produce(bytearray(msg, "utf-8"))
            time.sleep(0.5)

    except (MemphisError, MemphisConnectError, MemphisHeaderError, MemphisSchemaError) as e:
        print(e)

    finally:
        await memphis.close()

if __name__ == "__main__":
    for key in [HOST_KEY, USERNAME_KEY, PASSWORD_KEY, STATION_KEY]:
        if key not in os.environ:
            logging.error("Expected environmental variable {} not set".format(key))
            sys.exit(1)

    asyncio.run(main())

from __future__ import annotations
import asyncio
import time

from memphis import Memphis, Headers, MemphisError, MemphisConnectError, MemphisHeaderError, MemphisSchemaError

STATION = "todo-cdc-events"
USERNAME = "todocdcservice"
PASSWORD = "todocdcservice"
HOST = "localhost"

async def main():
    try:
        memphis = Memphis()
        await memphis.connect(host=HOST, username=USERNAME, password=PASSWORD)

        producer = await memphis.producer(station_name=STATION, producer_name="test-producer")
        msg = "This is a test message."
        while True:
            print("Sending message: {}".format(msg))
            await producer.produce(bytearray(msg, "utf-8"))
            time.sleep(0.5)

    except (MemphisError, MemphisConnectError, MemphisHeaderError, MemphisSchemaError) as e:
        print(e)

    finally:
        await memphis.close()

if __name__ == "__main__":
    asyncio.run(main())

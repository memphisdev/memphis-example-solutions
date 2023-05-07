from __future__ import annotations
import asyncio
import os

from memphis import Memphis, MemphisError, MemphisConnectError, MemphisHeaderError

STATION_KEY = "MEMPHIS_STATION"
USERNAME_KEY = "MEMPHIS_USERNAME"
PASSWORD_KEY = "MEMPHIS_PASSWORD"
HOST_KEY = "MEMPHIS_HOST"
        
async def main():
    async def msg_handler(msgs, error, context):
        try:
            for msg in msgs:
                print("message: ", msg.get_data())
                await msg.ack()
                headers = msg.get_headers()
                if error:
                    print(error)
        except (MemphisError, MemphisConnectError, MemphisHeaderError) as e:
            print(e)
            return
        
    try:
        print("Waiting on messages...")
        memphis = Memphis()
        await memphis.connect(host=os.environ[HOST_KEY],
                              username=os.environ[USERNAME_KEY],
                              password=os.environ[PASSWORD_KEY])
        
        consumer = await memphis.consumer(station_name=os.environ[STATION_KEY], consumer_name="printing-consumer", consumer_group="")
        consumer.consume(msg_handler)
        # Keep your main thread alive so the consumer will keep receiving data
        await asyncio.Event().wait()
        
    except (MemphisError, MemphisConnectError) as e:
        print(e)
        
    finally:
        await memphis.close()
        
if __name__ == '__main__':
    for key in [HOST_KEY, USERNAME_KEY, PASSWORD_KEY, STATION_KEY]:
        if key not in os.environ:
            logging.error("Expected environmental variable {} not set".format(key))
            sys.exit(1)    

    asyncio.run(main())

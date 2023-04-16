from __future__ import annotations
import asyncio
from memphis import Memphis, MemphisError, MemphisConnectError, MemphisHeaderError

STATION = "todo-cdc-events"
USERNAME = "todocdcservice"
PASSWORD = "todocdcservice"
HOST = "localhost"
        
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
        await memphis.connect(host=HOST, username=USERNAME, password=PASSWORD)
        
        consumer = await memphis.consumer(station_name=STATION, consumer_name="test-consumer", consumer_group="")
        consumer.consume(msg_handler)
        # Keep your main thread alive so the consumer will keep receiving data
        await asyncio.Event().wait()
        
    except (MemphisError, MemphisConnectError) as e:
        print(e)
        
    finally:
        await memphis.close()
        
if __name__ == '__main__':
    asyncio.run(main())

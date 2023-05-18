from __future__ import annotations
import asyncio
import json
import logging
import os
import sys

from memphis import Memphis, MemphisError, MemphisConnectError, MemphisHeaderError

INPUT_STATION_KEY = "MEMPHIS_INPUT_STATION"
OUTPUT_STATION_KEY = "MEMPHIS_OUTPUT_STATION"
USERNAME_KEY = "MEMPHIS_USERNAME"
PASSWORD_KEY = "MEMPHIS_PASSWORD"
HOST_KEY = "MEMPHIS_HOST"

def deserialize_mongodb_cdc_event(input_msg):
    """
    For MongoDB, Debezium returns the payload before and after fields as
    serialized JSON objects rather than subdocuments.  This function
    deserializes the JSON object, replaces the strings with JSON subdocuments,
    and then reserializes the entire message back to a bytearray.
    """

    obj = json.loads(input_msg)

    if "payload" in obj:
        payload = obj["payload"]

        if "before" in payload:
            before_payload = payload["before"]
            if before_payload is not None:
                payload["before"] = json.loads(before_payload)

        if "after" in payload:
            after_payload = payload["after"]
            if after_payload is not None:
                payload["after"] = json.loads(after_payload)

    output_s = json.dumps(obj)
    output_msg = bytearray(output_s, "utf-8")

    return output_msg

def create_handler(producer):
    """
    The interface for consumer.consume() takes an async function
    to handle the messages.  It doesn't provide a way to pass
    parameters, however.  I'm attempting to use a closure
    to workaround this.
    """
    async def msg_handler(msgs, error, context):
        try:
            for msg in msgs:
                print(type(msg), msg.get_data())
                transformed_msg = deserialize_mongodb_cdc_event(msg.get_data())
                print(type(transformed_msg), transformed_msg)
                print("Sending transformed message")
                await producer.produce(message=transformed_msg, async_produce=True)
                print("acknowledging initial message")
                await msg.ack()
                print("acknowledged")
                print()

        except (MemphisError, MemphisConnectError, MemphisHeaderError) as e:
            print(e)
            return

    return msg_handler

async def main():
    try:
        print("Waiting on messages...")
        memphis = Memphis()
        await memphis.connect(host=os.environ[HOST_KEY],
                              username=os.environ[USERNAME_KEY],
                              password=os.environ[PASSWORD_KEY])

        print("Creating consumer")
        consumer = await memphis.consumer(station_name=os.environ[INPUT_STATION_KEY],
                                          consumer_name="transformer",
                                          consumer_group="")

        print("Creating producer")
        producer = await memphis.producer(station_name=os.environ[OUTPUT_STATION_KEY],
                                          producer_name="transformer")

        print("Creating handler")
        msg_handler = create_handler(producer)

        print("Setting handler")
        consumer.consume(msg_handler)
        # Keep your main thread alive so the consumer will keep receiving data
        await asyncio.Event().wait()
        
    except (MemphisError, MemphisConnectError) as e:
        print(e)
        
    finally:
        await memphis.close()
        
if __name__ == '__main__':
    for key in [HOST_KEY, USERNAME_KEY, PASSWORD_KEY, INPUT_STATION_KEY, OUTPUT_STATION_KEY]:
        if key not in os.environ:
            logging.error("Expected environmental variable {} not set".format(key))
            sys.exit(1)    

    asyncio.run(main())

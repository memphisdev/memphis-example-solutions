#!/usr/bin/env python

import datetime as dt
import os
import random
import time
import sys

import psycopg2

HOST_KEY = "POSTGRES_HOST"
PASSWORD_KEY = "POSTGRES_PASSWORD"
USERNAME_KEY = "POSTGRES_USERNAME"

PORT_KEY = "POSTGRES_PORT"
DEFAULT_PORT = 5432

DATABASE_NAME = "todo_application"

DESCRIPTION_LENGTH = 20
ASCII_START = 65 # uppercase A
ASCII_END = 90 # uppercase Z

QUERY = "INSERT INTO todo_items (description, creation_date, due_date, completed) VALUES (%s, %s, %s, %s)"

if __name__ == "__main__":
    for key in [HOST_KEY, PASSWORD_KEY, USERNAME_KEY]:
        if key not in os.environ:
            msg = "Must specify environmental variable {}".format(key)
            print(msg)
            sys.exit(1)

    database_uri = "postgresql://{}:{}@{}:{}/{}".format(os.environ.get(USERNAME_KEY),
                                                        os.environ.get(PASSWORD_KEY),
                                                        os.environ.get(HOST_KEY),
                                                        os.environ.get(PORT_KEY, DEFAULT_PORT),
                                                        DATABASE_NAME)

    with psycopg2.connect(database_uri) as conn:
        with conn.cursor() as cur:
            while True:
                # generate a todo item
                creation_date = dt.datetime.now()
                due_date = None
                if random.random() < 0.5:
                    due_date = creation_date + dt.timedelta(days=3)

                chars = [chr(random.randint(ASCII_START, ASCII_END)) 
                            for i in range(DESCRIPTION_LENGTH)]
                description = "".join(chars)

                completed = False
                if random.random() < 0.1:
                    completed = True

                # insert into database
                cur.execute(QUERY, (description, creation_date, due_date, completed))
                conn.commit()

                print(description, creation_date, due_date, completed)

                # 0.5 sec delay between items
                time.sleep(0.5)

    conn.close()

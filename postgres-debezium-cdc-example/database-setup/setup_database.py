#!/usr/bin/env python

import os
import sys

import psycopg2

HOST_KEY = "POSTGRES_HOST"
USER_PASSWORD_KEY = "POSTGRES_USER_PASSWORD"
ADMIN_PASSWORD_KEY = "POSTGRES_ADMIN_PASSWORD"

PORT_KEY = "POSTGRES_PORT"
DEFAULT_PORT = 5432

ADMIN_DATABASE = "postgres"
ADMIN_USER = "postgres"
SERVICE_USER = "todo_service"

DATABASE_NAME = "todo_application"

if __name__ == "__main__":
    for key in [HOST_KEY, USER_PASSWORD_KEY, ADMIN_PASSWORD_KEY]:
        if key not in os.environ:
            msg = "Must specify environmental variable {}".format(key)
            print(msg)
            sys.exit(1)

    admin_uri = "postgresql://{}:{}@{}:{}/{}".format(ADMIN_USER,
                                               os.environ.get(ADMIN_PASSWORD_KEY),
                                               os.environ.get(HOST_KEY),
                                               os.environ.get(PORT_KEY, DEFAULT_PORT),
                                               ADMIN_DATABASE)

    with psycopg2.connect(admin_uri) as conn:
        with conn.cursor() as cur:
            # need to disable transactions to create / remove databases
            cur.execute("ABORT TRANSACTION;")
            # I tried using SQL parameters but psycopg2 quotes the strings
            cur.execute("DROP DATABASE IF EXISTS {};".format(DATABASE_NAME))
            cur.execute("CREATE DATABASE {};".format(DATABASE_NAME))
    conn.close()

    database_uri = "postgresql://{}:{}@{}:{}/{}".format(ADMIN_USER,
                                                   os.environ.get(ADMIN_PASSWORD_KEY),
                                                   os.environ.get(HOST_KEY),
                                                   os.environ.get(PORT_KEY, DEFAULT_PORT),
                                                   DATABASE_NAME)

    with psycopg2.connect(database_uri) as conn:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS todo_items;")

            cur.execute("CREATE TABLE todo_items ("
                        "item_id integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY, "
                        "description text NOT NULL, "
                        "due_date timestamp, "
                        "completed boolean NOT NULL "
                        ");")

            cur.execute("DROP ROLE IF EXISTS {};".format(SERVICE_USER))
            cur.execute("CREATE USER {} WITH PASSWORD '{}';".format(SERVICE_USER,
                                                            os.environ.get(USER_PASSWORD_KEY)))
            cur.execute("GRANT SELECT, INSERT, UPDATE, DELETE ON todo_items TO {};".format(SERVICE_USER))

        conn.commit()

    conn.close()

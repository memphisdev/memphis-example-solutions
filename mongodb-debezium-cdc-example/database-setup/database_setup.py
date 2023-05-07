#!/usr/bin/env python

import datetime as dt
import os
import random
import time
import sys

from pymongo import MongoClient

HOST_KEY = "MONGO_HOSTS"
PASSWORD_KEY = "MONGO_PASSWORD"
USERNAME_KEY = "MONGO_USERNAME"
REPLICA_SET_KEY = "REPLICA_SET"

if __name__ == "__main__":
    for key in [HOST_KEY, USERNAME_KEY, PASSWORD_KEY, REPLICA_SET_KEY]:
        if key not in os.environ:
            msg = "Must specify environmental variable {}".format(key)
            print(msg)
            sys.exit(1)

    # we expect something like "host1:port1,host2:port2,host3:port3"
    hosts_str = os.environ.get(HOST_KEY)
    hosts = hosts_str.split(",")

    direct_host = hosts[0].split(":")[0]
    direct_port = int(hosts[0].split(":")[1])
    username = os.environ.get(USERNAME_KEY)
    password = os.environ.get(PASSWORD_KEY)

    replica_set = os.environ.get(REPLICA_SET_KEY)

    members = []
    for idx, host in enumerate(hosts):
        members.append({
            "_id" : idx,
            "host" : host
        })

    config = {
        "_id" : replica_set,
        "members" : members
    }

    # taken from https://pymongo.readthedocs.io/en/stable/examples/high_availability.html
    client = MongoClient(direct_host, direct_port, directConnection=True, username=username, password=password)
    client.admin.command("replSetInitiate", config)
    client.close()

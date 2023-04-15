# postgres-debezium-cdc-example

## Running
You can run the example using Docker compose like so:

```bash
$ docker compose up --build -d
```

# Items to Add
1. List of services and ports
1. List of usernames and passwords

# Steps

1. `docker compose up -d` to start Postgres
1. Setup virtual environment: `python3 -m venv venv`
1. Start virtual environment: `source venv/bin/activate`
1. Update: `pip install -U pip wheel`
1. Update: `pip install -r requirements.txt`
1. Create schema: `POSTGRES_ADMIN_PASSWORD=postgres POSTGRES_USER_PASSWORD=postgres POSTGRES_HOST=localhost python setup_database.py`
1. Start REST server: `python deb_reciever.py`
1. Download
1. Untar
1. Make data directory
1. Copy `application.properties` to `conf` directory
1. Start Debezium Server: `./run.sh`
1. Connect to database: `psql -U postgres -h localhost todo_application`
1. Check that Debezium created a replication slot: `SELECT * FROM pg_replication_slots;`
1. Insert some records: `insert into todo_items (description, completed) values ('test1', false);`
1. Check the output logs of the REST service to see events printed as JSON

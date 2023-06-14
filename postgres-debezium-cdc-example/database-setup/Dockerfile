FROM python:3-slim

WORKDIR /app
COPY setup_database.py /app/

RUN pip3 install -U pip wheel
RUN pip3 install psycopg2-binary

CMD python3 setup_database.py

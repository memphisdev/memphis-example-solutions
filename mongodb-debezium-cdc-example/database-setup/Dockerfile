FROM python:3-slim

WORKDIR /app
COPY database_setup.py /app/

RUN pip3 install -U pip wheel
RUN pip3 install pymongo

CMD python3 database_setup.py

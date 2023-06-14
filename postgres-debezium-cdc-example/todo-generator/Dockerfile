FROM python:3-slim

WORKDIR /app
COPY todo_generator.py /app/

RUN pip3 install -U pip wheel
RUN pip3 install psycopg2-binary

CMD python3 todo_generator.py

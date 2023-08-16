FROM python:3-slim

WORKDIR /app
COPY upload_data.py /app/
COPY *.gz /app/

RUN pip3 install -U pip wheel
RUN pip3 install memphis-py pandas tqdm

CMD python3 upload_data.py --transactions-fl transactions.tsv.gz --line-items-fl line_items.tsv.gz

FROM python:3.8

RUN apt-get install wget
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY csv_processing.py csv_processing.py

ENTRYPOINT [ "python", "csv_processing.py" ]
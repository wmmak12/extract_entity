# Use the official lightweight Python image.
FROM python:3.9-slim

# Install sqlite
RUN apt-get -y update && apt-get install -y sqlite3
RUN apt-get -y install gcc

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy files into docker
WORKDIR /usr/extract_entity/
COPY . .

# Install python dependencies and set workdir
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /usr/extract_entity/src

# Install spacy content
RUN python -m spacy download en_core_web_sm

# Create a new table to store collected info into sqlite
RUN python3 create_sqlite_db.py

# Main API service Command
CMD ["gunicorn", "--workers", "5", "--worker-class", "meinheld.gmeinheld.MeinheldWorker", "--timeout", "120", "-b", ":$PORT", "extract_entity_api:__hug_wsgi__"]


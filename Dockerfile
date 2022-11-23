FROM python:3.10-slim-buster

WORKDIR /service

COPY ./requirements.txt .

RUN apt-get update
RUN apt-get install libxslt-dev libxml2-dev libpam-dev libedit-dev -y
RUN apt-get install libpq-dev -y
RUN apt-get install build-essential -y

RUN pip install --upgrade pip --ignore-installed

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["sh","./entrypoint.sh"]

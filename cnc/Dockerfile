# Use an official Python runtime as a parent image
FROM alpine:3.4

RUN apk add --no-cache bind-tools python py-pip wireshark-common

WORKDIR /app

ADD . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN mkdir /logs

EXPOSE 80

ENV FLASK_ENV dockerdns

CMD ["python", "app.py"]

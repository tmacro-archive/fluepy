FROM gliderlabs/alpine:latest

RUN apk-install python3

ADD . /app
WORKDIR /app

RUN pip3 install -r requirements.txt

CMD python3 flue.py

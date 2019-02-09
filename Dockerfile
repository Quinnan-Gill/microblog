FROM python:3.6-alpine

RUN adduser -D microblog

WORKDIR /home/microblog

RUN apk add --no-cache curl python pkgconfig python-dev openssl-dev libffi-dev musl-dev make gcc

COPY requirements.txt requirements.txt 
RUN python -m venv venv 
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt 
RUN venv/bin/pip install gunicorn
RUN venv/bin/pip install gunicorn pymysql

COPY app app 
COPY migrations migrations 
COPY microblog.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP microblog.py 

RUN chown -R microblog:microblog ./
USER microblog

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
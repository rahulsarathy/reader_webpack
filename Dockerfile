FROM python:3.6-alpine

RUN adduser -D reader

WORKDIR /home/reader

COPY requirements.txt requirements.txt

RUN apk add --update --no-cache g++ gcc libxslt-dev
RUN apk add build-base python-dev py-pip jpeg-dev zlib-dev
ENV LIBRARY_PATH=/lib:/usr/lib

RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip3 install newspaper3k && \
    curl https://raw.githubusercontent.com/codelucas/newspaper/master/download_corpora.py | python3
RUN venv/bin/pip install gunicorn

COPY app app
COPY static static
COPY EPUB_Template EPUB_Template
COPY publishing publishing
COPY migrations migrations
COPY reader.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP reader.py

RUN chown -R reader:reader ./
USER reader

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
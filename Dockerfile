FROM python:3.6-alpine

RUN adduser -D reader

WORKDIR /home/reader

COPY ./server/requirements.txt requirements.txt
RUN python -m venv venv
RUN ./server/venv/bin/pip install -r requirements.txt
RUN ./server/venv/bin/pip install gunicorn

COPY ./server/app app
COPY ./server/migrations migrations
COPY ./server/reader.py ./server/config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP ./server/reader.py

RUN chown -R reader:reader ./
USER reader

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
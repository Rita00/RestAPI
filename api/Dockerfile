FROM python:3.9.4

ADD main.py /
ADD modules /
ADD modules/Database.py /modules/Database.py

RUN pip install flask

RUN pip install psycopg2

EXPOSE 8080
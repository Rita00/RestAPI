FROM python:3.9.4

ENV POSTGRES_USER bidyourauction
ENV POSTGRES_PASSWORD bidyourauction
ENV POSTGRES_DB bidyourauction_db

ADD main.py /
ADD modules /
ADD modules/Database.py /modules/Database.py

RUN pip install flask

RUN pip install psycopg2

EXPOSE 8080

CMD ["python", "main.py"]
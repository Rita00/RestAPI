FROM python:3.9.4

ENV BIDYOURAUCTION_USER bidyourauction
ENV BIDYOURAUCTION_PASSWORD bidyourauction
ENV BIDYOURAUCTION_DB bidyourauction_db

ADD main.py /
ADD modules /
ADD modules/Database.py /modules/Database.py

RUN pip install flask
RUN pip install jwt
RUN pip install psycopg2

EXPOSE 8080

CMD ["python", "main.py"]
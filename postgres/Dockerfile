FROM library/postgres

ENV POSTGRES_USER bidyourauction
ENV POSTGRES_PASSWORD bidyourauction
ENV POSTGRES_DB bidyourauction_db

COPY data.sql /docker-entrypoint-initdb.d/

EXPOSE 5432
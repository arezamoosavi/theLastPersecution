#!/bin/sh


set -o errexit
set -o nounset

airflow db init
sleep 2
airflow users create \
          --username admin \
          --firstname admin \
          --lastname admin \
          --password admin \
          --role Admin \
          --email email@email.com

airflow webserver -p 8000 &\
sleep 2 &\
airflow scheduler &\
sleep 2 &\
airflow celery worker -q default &\
sleep 2 &\
airflow celery flower -a sqla+postgresql://admin:admin@postgres:5432/celery

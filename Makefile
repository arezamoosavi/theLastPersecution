.PHONY: jars_dl pg airflow down

jars_dl:
	sh jarfile_download.sh

clear-images:
	docker image prune --filter="dangling=true"

pg:
	docker-compose up -d postgres

build-spark:
	docker-compose up --build -d spark

exec-spark:
	docker-compose exec spark bash

stop-spark:
	docker-compose stop spark
	echo y | docker-compose rm spark

airflow:
	docker-compose up -d airflow
	sleep 5
	docker-compose up -d airflow-spark-queue

scale-spark-queue:
	docker-compose scale airflow-spark-queue=3

stop-airflow:
	docker-compose stop airflow airflow-spark-queue
	echo y | docker-compose rm airflow airflow-spark-queue

down:
	docker-compose down -v
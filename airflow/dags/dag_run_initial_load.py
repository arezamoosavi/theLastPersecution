from __future__ import print_function

from datetime import datetime

import airflow
from airflow.operators.bash_operator import BashOperator

args = {
    "owner": "airflow",
    "provide_context": True,
    "catchup": False,
}

dag = airflow.DAG(
    dag_id="initial_etl",
    default_args=args,
    start_date=datetime(year=2021, month=9, day=19),
    schedule_interval="@once",
    max_active_runs=1,
    concurrency=1,
)

start_task = BashOperator(
    task_id="start_task",
    queue='default',
    bash_command="echo this task started at : {{ ds }}",
    dag=dag,
)

task_spark_load = BashOperator(
    task_id="spark_initial_load_data",
    queue='spark',
    bash_command="spark-submit "
    "--master spark://spark-master:7077 "
    "--deploy-mode client "
    "--driver-memory 2g --num-executors 1 "
    "--jars /opt/airflow/dags/etl/jars/postgresql-42.2.5.jar "
    "--py-files /opt/airflow/dags/etl/utils/common.py "
    "/opt/airflow/dags/etl/spark_load_data.py",
    dag=dag,
)

task_spark_transform = BashOperator(
    task_id="spark_initial_transform_data",
    queue='spark',
    bash_command="spark-submit "
    "--master spark://spark-master:7077 "
    "--deploy-mode client "
    "--driver-memory 2g --num-executors 1 "
    "--jars /opt/airflow/dags/etl/jars/postgresql-42.2.5.jar "
    "--py-files /opt/airflow/dags/etl/utils/common.py "
    "/opt/airflow/dags/etl/spark_transform_data.py",
    dag=dag,
)


start_task >> task_spark_load >> task_spark_transform
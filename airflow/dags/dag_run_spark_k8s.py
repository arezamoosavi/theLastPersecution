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
    bash_command="""spark-submit --verbose --master k8s://https://192.168.0.1:6443 \
	--deploy-mode cluster \
	--py-files local:///opt/work-dir/utils/common.py \
	--conf spark.kubernetes.authenticate.submission.caCertFile={{var.value.airflow_home}}/dags/certificate.pem \
	--conf spark.kubernetes.authenticate.submission.oauthToken={{var.value.spark_token}} \
	--conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
	--conf spark.kubernetes.driver.pod.name=bitcoin-load-app \
	--conf spark.kubernetes.container.image.pullPolicy=Always \
	--conf spark.executor.instances=2 \
	--conf spark.executor.memory=2G \
	--conf spark.executor.cores=1 \
	--conf spark.driver.memory=1G \
	--conf spark.kubernetes.container.image=192.168.0.1:5000/main-spark:latest \
	--name bitcoin-app1 \
	--jars local:///opt/spark/jars/postgresql-42.2.5.jar \
	local:///opt/work-dir/spark_load_data.py 192.168.0.1
    """,
    dag=dag,
)

task_spark_transform = BashOperator(
    task_id="spark_initial_transform_data",
    queue='spark',
    bash_command="""spark-submit --verbose --master k8s://https://192.168.0.1:6443 \
	--deploy-mode cluster \
	--py-files local:///opt/work-dir/utils/common.py \
	--conf spark.kubernetes.authenticate.submission.caCertFile={{var.value.airflow_home}}/dags/certificate.pem \
	--conf spark.kubernetes.authenticate.submission.oauthToken={{var.value.spark_token}} \
	--conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
	--conf spark.kubernetes.driver.pod.name=bitcoin-transfer-app \
	--conf spark.kubernetes.container.image.pullPolicy=Always \
	--conf spark.executor.instances=2 \
	--conf spark.executor.memory=2G \
	--conf spark.executor.cores=1 \
	--conf spark.driver.memory=1G \
	--conf spark.kubernetes.container.image=192.168.0.1:5000/main-spark:latest \
	--name bitcoin-app2 \
	--jars local:///opt/spark/jars/postgresql-42.2.5.jar \
	local:///opt/work-dir/spark_transform_data.py 192.168.0.1
    """,
    dag=dag,
)


start_task >> task_spark_load >> task_spark_transform

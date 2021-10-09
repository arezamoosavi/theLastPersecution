set-params-ip:
	docker network inspect bridge
	code /etc/docker/daemon.json
	# "default-address-pools": [{"base":"192.168.0.191/16","size":24}],
	# "nsecure-registries":["192.168.0.1:5000"]
	sudo systemctl daemon-reload
	sudo systemctl restart docker

install-kind:
	curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.11.1/kind-linux-amd64
	chmod +x ./kind
	mv ./kind /some-dir-in-your-PATH/kind
kind-dash:
	kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.1.0/aio/deploy/recommended.yaml
	kubectl get pod -n kubernetes-dashboard
	kubectl create clusterrolebinding default-admin --clusterrole cluster-admin --serviceaccount=default:default
	token=$(kubectl get secrets -o jsonpath="{.items[?(@.metadata.annotations['kubernetes\.io/service-account\.name']=='default')].data.token}"|base64 --decode)
	echo ${token}
	kubectl proxy
	#http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#/login

start-cluster:
	sh kind-with-registry.sh

docker-images:
	docker container ls
	docker images

docker-tag:
	docker tag thelastpersecution_spark 192.168.0.1:5000/main-spark:latest

docker-push:
	docker push 192.168.0.1:5000/main-spark:latest

check-registry:
	curl -X GET http://192.168.0.1:5000/v2/main-spark/tags/list

kind-cmd:
	kind get clusters
	kubectl cluster-info --context kind-kind
	kind delete cluster

all-deploy:
	kubectl apply -f deployment/

delete-all-deploy:
	kubectl delete -f deployment/

logging:
	kubectl delete daemonsets,replicasets,services,deployments,pods,rc --all
	kubectl delete all --all --all-namespaces
	kubectl get pods --field-selector 'status.phase=Failed' -o name | xargs kubectl delete
	kubectl get all
	kubectl logs -f pod/pod-id
	kubectl port-forward --address 0.0.0.0 service/spark-master 8080:8080 18080:18080 7077:7077 &
	kubectl port-forward --address 0.0.0.0 pod/locations-streaming-4b74cd78597bef51-driver 4040:4040 &
	kubectl proxy --address='0.0.0.0' --port=36273 --accept-hosts='.*' &


setup_k8s:
	kubectl create serviceaccount spark
	kubectl create clusterrolebinding spark-role --clusterrole=edit  --serviceaccount=default:spark --namespace=default
	kubectl get secrets -o jsonpath="{.items[?(@.metadata.annotations['kubernetes\.io/service-account\.name']=='spark')].data.token}"|base64 --decode && echo
	echo -n|openssl s_client -connect 192.168.0.1:6443|openssl x509 -outform PEM > ../airflow/dags/certificate.pem
	
	kubectl get secret
	kubectl describe secret spark-token
	# add this token to spark-submit
	kubectl cluster-info

run-on-k8s-cluster:
	kubectl cluster-info
	./bin/spark-submit --verbose --master k8s://https://192.168.0.1:6443 --deploy-mode cluster --py-files local:///opt/work-dir/utils/common.py --conf spark.kubernetes.container.image.pullPolicy=Always --conf spark.executor.instances=1 --conf spark.executor.memory=2G --conf spark.executor.cores=1 --conf spark.driver.memory=1G --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark --conf spark.kubernetes.container.image=192.168.0.1:5000/main-spark:latest --jars local:///opt/spark/jars/postgresql-42.2.5.jar local:///opt/work-dir/spark_load_data.py 192.168.0.1


run-airflow-spark:
	spark-submit --verbose --master k8s://https://192.168.0.1:6443 \
	--deploy-mode cluster \
	--py-files local:///opt/work-dir/utils/common.py \
	--conf spark.kubernetes.authenticate.submission.caCertFile=dags/certificate.pem \
	--conf spark.kubernetes.authenticate.submission.oauthToken=${spark_token} \
	--conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
	--conf spark.kubernetes.driver.pod.name=bitcoin-app \
	--conf spark.kubernetes.container.image.pullPolicy=Always \
	--conf spark.executor.instances=1 \
	--conf spark.executor.memory=2G \
	--conf spark.executor.cores=1 \
	--conf spark.driver.memory=1G \
	--conf spark.kubernetes.container.image=192.168.0.1:5000/main-spark:latest \
	--name bitcoin-app \
	--jars local:///opt/spark/jars/postgresql-42.2.5.jar \
	local:///opt/work-dir/spark_load_data.py 192.168.0.1
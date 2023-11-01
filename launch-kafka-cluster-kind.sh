# Creating kind cluster
sudo kind create cluster --config kind/kind.yaml

# Creating namespaces
kubectl create namespace kafka
#kubectl create namespace monitoring
kubectl create namespace spark-operator
#kubectl create namespace mongodb-database
kubectl create namespace airflow

# Set airflow configmap volumes
#kubectl apply -f airflow/requirements-configmap.yaml

# Set docker and aws credentials
kubectl apply -f ../kind-kafka/secrets/secret-docker.yaml
#kubectl apply -f secrets/secret-aws.yaml

# Installing Strimzi
helm repo add strimzi https://strimzi.io/charts/
helm install strimzi strimzi/strimzi-kafka-operator -f strimzi/strimzi-values.yaml -n kafka

# Give a time to install Strimzi
sleep 120

# Install mongo-operator
#helm repo add mongodb https://mongodb.github.io/helm-charts
#helm install mongodb mongodb/community-operator -f mongo/mongo-operator-values.yaml -n mongodb-database

# Installing spark-operator
helm repo add spark-operator https://googlecloudplatform.github.io/spark-on-k8s-operator
helm install spark-operator spark-operator/spark-operator -f spark/spark-operator-values.yaml -n spark-operator

# Deploying airflow
#helm install airflow oci://registry-1.docker.io/bitnamicharts/airflow -n airflow -f airflow/airflow.yaml
helm repo add apache-airflow https://airflow.apache.org
helm upgrade --install airflow apache-airflow/airflow --namespace airflow -f airflow/airflow.yaml

# Installing prometheus
#helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
#helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring

# Deploying mongo and service for external access
#kubectl apply -f mongo/mongo-deploy.yaml
#kubectl apply -f mongo/mongo-service.yaml

# Deploying Kafka and zookeper for Strimzi
kubectl apply -f strimzi/kafka-deploy.yaml -n kafka
kubectl wait kafka/my-cluster --for=condition=Ready --timeout=600s -n kafka

# Installing kafka-exporter for prometheus monitoring
#helm install kafka-exporter prometheus-community/prometheus-kafka-exporter -f strimzi/kafka-exporter-values.yaml -n kafka

# Installing schema-registry using bitnami helm-charts - submitted an issue @ https://github.com/bitnami/charts/issues/18237
#helm install schema-registry oci://registry-1.docker.io/bitnamicharts/schema-registry -n kafka -f strimzi/schema-registry-values.yaml

# Deploying ksqldb for kafka - using ksqldb API for request purposes - see python-applications
#kubectl apply -f ksqldb/ksqldb-deploy.yaml

# define permissions
kubectl create clusterrolebinding default-pod --clusterrole cluster-admin --serviceaccount=spark-operator:default
kubectl create clusterrolebinding default-pod2 --clusterrole cluster-admin --serviceaccount=airflow:default
kubectl create clusterrolebinding default-pod3 --clusterrole cluster-admin --serviceaccount=airflow:airflow-worker
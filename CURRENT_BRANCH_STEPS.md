# Install Minikube

https://minikube.sigs.k8s.io/docs/start/


# Install helm

https://helm.sh/docs/intro/install/


# Install helm dependencies

`helm dependencies update`


# Install helm chart
eval $(minikube docker-env)
docker build -t catalog:latest .
helm install release-name . --values values.yaml -n test --create-namespace

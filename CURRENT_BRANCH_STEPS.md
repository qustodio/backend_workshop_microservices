# Install Minikube

https://minikube.sigs.k8s.io/docs/start/


# Run Minikube

`minikube start`


# Install plugins

`minikube addons enable ingress`


# Install helm

https://helm.sh/docs/intro/install/


# Install helm dependencies
```
cd helm
helm dependencies update
```


# Install helm chart
Replace `{{ release-name }}` and `{{ release-namespace }}` with the actual values you wish to use
```
eval $(minikube docker-env)
docker build -t catalog:latest .
helm install {{ release-name }} . --values values.yaml -n {{ release-namespace }} --create-namespace
```

# Access the application

Get minikube's IP:
`minikube ip`

Add the following line to your `/etc/hosts` file (being {{ MINIKUBE_IP }} the IP obtained with the previous command):
`{{ MINIKUBE_IP }} qbooks.com`

You can now access your application's ingress withyour browser by just accessing `qbooks.com`


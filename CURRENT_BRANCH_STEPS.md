# Install Minikube

https://minikube.sigs.k8s.io/docs/start/


# Run Minikube

`minikube start`


# Install plugins

`minikube addons enable ingress`


# Run dashboard

`minikube dashboard`


# Install helm

https://helm.sh/docs/intro/install/


# Install helm dependencies

```
helm dependencies update ./chart
```


# Install helm chart

Replace `RELEASE-NAME` and `RELESE-NAMESPACE` with the actual values you wish to use
```
# We need to run the following command to ensure we build our images with minikube's docker agent.
# If we don't, even if you build your images, minikube won't be able to access them.
eval $(minikube docker-env)

# Build our image
docker build -t catalog:latest .

# Deploy our chart on minikube
helm install RELEASE-NAME ./chart --values ./chart/values.yaml -n RELEASE-NAMESPACE --create-namespace
```

# Access the application

Get minikube's IP:
`minikube ip`

Add the following line to your `/etc/hosts` file (being MINIKUBE_IP the IP obtained with the previous command):
`MINIKUBE_IP qbooks.com`

You can now access your application's ingress withyour browser by just accessing `qbooks.com`


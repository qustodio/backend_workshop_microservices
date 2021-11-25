# Install Minikube

https://minikube.sigs.k8s.io/docs/start/


# Install Kubectl

https://kubernetes.io/docs/tasks/tools/#kubectl


# Run Minikube

```
minikube start

# Needed to use istio's ingress
minikube tunnel
```


# Install plugins

`minikube addons enable ingress`


# Run dashboard

`minikube dashboard`


# Install helm

https://helm.sh/docs/intro/install/


# Install istio

```
helm repo add istio https://istio-release.storage.googleapis.com/charts
helm repo update

kubectl create namespace istio-system
helm install istio-base istio/base -n istio-system

helm install istiod istio/istiod -n istio-system --wait

kubectl create namespace istio-ingress
kubectl label namespace istio-ingress istio-injection=enabled
helm install istio-ingress istio/gateway -n istio-ingress --wait
```


# Set up namespace for our app

```
kubectl create namespace qbooks
kubectl label namespace qbooks istio-injection=enabled
```


# Install helm dependencies

```
helm dependencies update ./chart
```


# Install helm chart

Replace `RELEASE-NAME` with the actual values you wish to use
```
# We need to run the following command to ensure we build our images with minikube's docker agent.
# If we don't, even if you build your images, minikube won't be able to access them.
eval $(minikube docker-env)

# Build our image
docker build -t catalog:latest .

# Deploy our chart on minikube on the qbook namespace
helm install RELEASE-NAME ./chart --values ./chart/values.yaml -n qbooks
```

# Access the application

## Kubernetes ingress
Get minikube's IP:
```
minikube ip
```

Add the following line to your `/etc/hosts` file (being MINIKUBE_IP the IP obtained with the previous command):
```
MINIKUBE_IP qbooks.com
```

You can now access your application's ingress withyour browser by just accessing `qbooks.com`


## Istio ingress gateway

Get the ingress' external IP:
```
kubectl get svc istio-ingress -n istio-ingress
```

Add the following line to your `/etc/hosts` file (being ISTIO_INGRESS_EXTERNAL_IP the IP obtained with the previous command):
```
ISTIO_INGRESS_EXTERNAL_IP qbooks.com
```

You can now access your application's ingress withyour browser by just accessing `qbooks.com`


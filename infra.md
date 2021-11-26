# Setting-up the cluster
## What's about

Here we will setup a kubernetes cluster in our machine

## Kubectl

Kubectl is a cli to interact with kubernetes clusters

### Installation

https://kubernetes.io/docs/tasks/tools/#kubectl

## Helm

Helm is a package manager for kubernetes. It simplifies the installation of applications on kubernetes

### Installation

https://helm.sh/docs/intro/install/

## Minikube

Minikube is a local kubernetes that focuses on quickly set up a cluster to play around with.

### Installation

https://minikube.sigs.k8s.io/docs/start/

### Running minikube

```bash
# Minikube
minikube start

# Minikube tunnel, needed to use istio's ingress
minikube tunnel

# (Optional) Dashboard
minikube dashboard
```

### Install addons
```bash
minikube addons enable ingress
```


# Setting-up infrastructure
## What's about

Here we will add some amazing monitoring utils that will help us
to have observability within the cluster

## Istio

Istio is a service mesh for kubernetes. It allows us to simply observability, traffic management, security, and policies managent

### Steps

```bash
# Add helm repository
helm repo add istio https://istio-release.storage.googleapis.com/charts
helm repo update

# Install istio's base chart
kubectl create namespace istio-system
helm install istio-base istio/base -n istio-system

# Install istio's control plane
helm install istiod istio/istiod -n istio-system --wait

# Install istio's ingress
kubectl create namespace istio-ingress
kubectl label namespace istio-ingress istio-injection=enabled
helm install istio-ingress istio/gateway -n istio-ingress --wait
```

## Kube Prometheus stack

The 'Kube prometheus stack' is...

### Steps

Add the helm repository

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

We do create the namespace

```bash
kubectl create namespace prometheus-stack
```

Install the prometheus stack in its namespace
```bash
helm install prometheus-stack prometheus-community/kube-prometheus-stack --namespace prometheus-stack --values infra/kube-prometheus-stack/values.yml
```

## Loki

### Steps

Add the helm repository

```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```

We do create the namespace
```bash
kubectl create namespace loki-stack
```

Install the loki stack in its namespace
```bash
helm upgrade --install loki --namespace=loki-stack grafana/loki-stack --values infra/loki/values.yml
```

## Kiali

Kiali is a management console for Istio.

### Steps

```bash
# Add kiali helm repo
helm repo add kiali https://kiali.org/helm-charts
helm repo update

# Install kiali chart
helm install kiali-server kiali/kiali-server --namespace istio-system --values infra/kiali/values.yml
```

# Setting-up our application

## What's about

We will install our application on the cluster using Helm, and allow istio to inject its sidecars on our application's pods

## Namespace

### Create namespace

Create the kubernetes' namespace

```bash
kubectl create namespace qbooks
```

### Labels
Add istio's label to the namespace
```bash
kubectl label namespace qbooks istio-injection=enabled
```
This allows istio to inject a sidecard to our application's pods.
The sidecard will handle the pod's connectivity and networking to integrate it to the service mesh in a seamless way

## Helm chart

Install helm chart.

### Dependencies

Our chart has a dependencies to other chart. This command downloads the needed charts to complete our app's installation
```bash
helm dependencies update ./chart
```

### Docker images

Minikube uses it's own docker agent to manage its containers.
To make our local images available to minikube, we first need to load some environment variables provided by minikube, and then build our images.

```bash
eval $(minikube docker-env)
docker build -t catalog:latest .
```

### Install chart

Values files allows us to customize and tune properties of our helm installation.
We will install our application using the values file located in the chart's path.
```bash
helm install qbooks-app ./chart --values ./chart/values.yaml -n qbooks
```

# Accessing our application

## What's about

We will learn how to access our local application with the correct hostname.

### Ingress' IP

The cluster has an ingress configured. This ingress is the way kubernetes manages how external requests interact with its services.
To get the IP of the ingress, we need to run the following command:
```bash
kubectl get svc istio-ingress -n istio-ingress
```
We are interested in the external IP.

### Hosts file

We need to add an entry to the hosts file in our machine, to resolve the application's hostname to the ingress' IP.
Add the following line to the `/etc/hosts` file, replacing `X.X.X.X`with the ingress' IP:
`X.X.X.X    qbooks.com'`

### Access the application

Access `qbooks.com` with your browser


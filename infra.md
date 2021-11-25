# Setting-up infrastructure
## What's about

Here we will add some amazing monitoring utils that will help us
to have observability within the cluster

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


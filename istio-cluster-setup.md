# Istio Cluster Setup

This document details the steps to set up an Istio cluster for performance testing purposes.

[setup-istio-cluster-commands.txt](./setup-istio-cluster-commands.txt) file could be used for cross reference to commands.

## Prerequisites

* Kind cluster creation tool (https://kind.sigs.k8s.io/docs/user/quick-start/)
* Helm package manager (https://helm.sh/docs/helm/helm_install/)
* Locust performance testing tool (https://locust.io/)

## Cluster Creation

### Step 1: Verify Existing Clusters (Optional)

```bash
kind get clusters
```

This command lists any existing Kind clusters.

### Step 2: Create a New Kind Cluster
```bash
kind create cluster --config=cluster.yaml --name istio
```
Replace `cluster.yaml` with the path to your cluster configuration file if it differs.

### Step 3: Install Nginx Ingress
```bash
kubectl apply -f ingress-nginx.yaml
```
This command deploys the Nginx ingress controller into your cluster using the provided YAML file `ingress-nginx.yaml`.

### Step 4: Apply Helmsman Common Components
```bash
helmsman -f applications.yaml --apply
```

This command leverages Helmsman to deploy common components defined in `applications.yaml`.

### Step 5: Configure Grafana
**Port Forward Grafana Pod:**

Use `kubectl port-forward` to forward the Grafana pod port to your local machine for access. The specific pod name and port can be found using kubectl get pods.

**Add Prometheus Data Source:**

Within Grafana, configure a new data source using the Prometheus server address (e.g., http://prometheus-server.prometheus).

**Import Grafana Dashboards:**

Import the required Grafana dashboards with IDs `10856` and `15760`.

### Step 6: Wait for Metrics Collection
Allow the cluster some time (around 5 minutes) to collect performance metrics before proceeding.

### Step 7: Install Istio
Follow the official Istio documentation for installation steps: https://istio.io/latest/docs/setup/getting-started/#download

(Note: The recommended Istio version used in this research was 1.19.0)

**Run the following command to install Istio with the minimal profile:**
```bash
istioctl install --set profile=minimal -y
```

Refer to https://istio.io/latest/docs/setup/additional-setup/config-profiles/ for profile details.

### Step 8: Wait for Istio Integration
Allow another 5 minutes for Istio to integrate with your cluster after installation.

### Step 9: Enable Istio Injection on Namespaces
Label the desired namespaces (tenant1 and tenant2) for Istio sidecar injection:
```bash
kubectl label namespace tenant1 istio-injection=enabled
kubectl label namespace tenant2 istio-injection=enabled
```
Restart deployments within the labeled namespaces to ensure Istio proxy sidecar injection:
(Specific deployment restart commands might be required based on your deployment configuration)

### Step 10: Run Locust Tests
Execute Locust tests with the following configurations:

* 10 users, span rate 0.1, duration: 5 minutes
* 20 users, span rate 0.1, duration: 30 minutes

(The specific Locust command might differ based on your test setup)

### Step 11: Capture Data Points
Capture performance data points after each Locust test run for analysis.

This document provides a step-by-step guide to setting up an Istio cluster on Kind for performance testing purposes. Remember to replace placeholders like cluster.yaml and adjust commands based on your specific deployment configuration.
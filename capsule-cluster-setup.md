# Capsule Cluster Setup

This document details the steps to set up a Capsule cluster for performance testing purposes.

[setup-capsule-cluster-commands.txt](./setup-capsule-cluster-commands.txt) file could be used for cross reference to commands.


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

```
kind create cluster --config=cluster.yaml --name capsule
```
Replace `cluster.yaml` with the path to your cluster configuration file if it differs.

### Step 3: Install Nginx Ingress

```
kubectl apply -f ingress-nginx.yaml
```
This command deploys the Nginx ingress controller into your cluster using the provided YAML file `ingress-nginx.yaml`.

### Step 4: Apply Helmsman Common Components
```
helmsman -f applications.yaml --apply
```

This command leverages Helmsman to deploy common components defined in applications.yaml.

### Step 5: Configure Grafana
***Port Forward Grafana Pod:***

Use `kubectl port-forward` to forward the Grafana pod port to your local machine for access. The specific pod name and port can be found using kubectl get pods.

**Add Prometheus Data Source:**

Within Grafana, configure a new data source using the Prometheus server address (e.g., http://prometheus-server.prometheus).

**Import Grafana Dashboards:**

Import the required Grafana dashboards with IDs `10856` and `15760`.

### Step 6: Wait for Metrics Collection
Allow the cluster some time (around 5 minutes) to collect performance metrics before proceeding.

### Step 7: Install Capsule
```
kubectl apply -f https://raw.githubusercontent.com/clastix/capsule/master/config/install.yaml
```

*Potential First-Time Deployment Error:*

You might encounter an error message stating "no matches for kind "CapsuleConfiguration" in version "capsule.clastix.io/v1beta2"." This indicates that the Capsule Custom Resource Definitions (CRDs) need to be installed first.

*Resolving the Error:*

As suggested in https://github.com/projectcapsule/capsule/issues/368#issuecomment-892735970, re-running the same `kubectl apply` command above should resolve the issue.

### Step 8: Wait for Capsule Integration
Allow another 5 minutes for Capsule to integrate with your cluster after installation.

### Step 9: Create Tenants and Deploy Test Services
1. Create Tenants:
```
kubectl apply -f 1-create-tenants.yaml
```

2. Create Tenant Users:
Use the provided script `2-create-user.sh` to generate dummy users for testing purposes. The script can be found at https://github.com/projectcapsule/capsule/blob/main/hack/create-user.sh.

**Script Permissions and Usage:**
```
chmod +x 2-create-user.sh
sh ./2-create-user.sh tenant1-admin tenant1
sh ./2-create-user.sh tenant2-admin tenant2
```

These commands grant executable permissions to the script and then create dummy users `tenant1-admin` for `tenant1` and `tenant2-admin` for `tenant2`.

3. Deploy Test Services to Tenant Namespaces:
Important: These steps need to be executed from the Capsule directory.

* **Tenant 1:**
```
export KUBECONFIG=tenant1-admin-tenant1.kubeconfig
kubectl create ns tenant1
kubectl apply -f ../test-service/capsule/tenant1-echo-server.yaml
```

These commands:
* Set the `KUBECONFIG` environment variable to use the tenant administrator configuration file.
* Create the `tenant1` namespace.
* Deploy the test service `tenant1-echo-server.yaml` within the `tenant1` namespace.

* **Tenant 2 (similar process):**
```
export KUBECONFIG=tenant2-admin-tenant2.kubeconfig
kubectl create ns tenant
```

### Step 10: Run Locust Tests
Execute Locust tests with the following configurations:

* 10 users, span rate 0.1, duration: 5 minutes
* 20 users, span rate 0.1, duration: 30 minutes

(The specific Locust command might differ based on your test setup)
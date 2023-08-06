# How this works

The NMachine Prometheus Plugin connects to a Prometheus
server that is (or is capable of) monitoring your application.
<br/><br/>
This operation lets you point to the server. If the Prometheus
server is already configured to receive events from this cluster,
the plugin will work as soon as the operation finishes. 
<br/><br/>
**Note**: If you _do not_ have a Prometheus server that you can 
point to, find the "Create app-specific Prometheus Instance" operation.

## Option I: In-Cluster Prometheus Server

An in-cluster Prometheus server is most likely one installed via Helm,
such as [kube-prometheus-stack](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack) 
or [kube-prometheus](https://github.com/prometheus-operator/kube-prometheus),
but can also be from another source. 
<br/><br/>
The only requirement is that the 
workload that run the server that responds to /api/query be exposed
as a service.

#### NB: Out-of-cluster KAMAs

Note that if the KAMA you are using right now is outside of your cluster,
all calls to the Prometheus API will be proxied by Kubernetes, which may 
reduce performance by up to ~250ms every call.

## Option II: Out-of-Cluster Prometheus Server

If the Prometheus server is not hosted inside the cluster,
or Option I is not suitable, choose this option. Again, the 
only requirement is for the server to respond to /api/query.
<br/><br/>
If the server requires authentication, create a token from 
your Prometheus UI and paste it here.
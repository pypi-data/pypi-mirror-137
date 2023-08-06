# Todo

## Testing

For the tests to run, a Prometheus installation **must**
be running in your cluster with:
- namespace = `monitoring`
- main service = `monitoring-prometheus-server`. 

Use the 
**[Community Prometheus Helm Chart](https://artifacthub.io/packages/helm/prometheus-community/prometheus)**
to do this the easy way.  

In the future, these fields will be configurable via environment variables.
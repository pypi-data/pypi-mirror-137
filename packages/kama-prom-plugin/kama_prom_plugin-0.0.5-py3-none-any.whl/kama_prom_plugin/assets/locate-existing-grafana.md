# How this works

The NMachine Prometheus Plugin has limited interoperability with
Grafana. Namely, it provides a handy link (or port-forward), 
and it can report on the worload's health if it is in the cluster.

### If you don't have Grafana

That's okay. The plugin mainly uses the Prometheus API.
from kama_sdk.core.core.consts import KTEA_TYPE_SERVER
from kama_sdk.core.core.types import KteaDict

PLUGIN_ID = 'nmachine.prom'
STRATEGY_KEY = "strategy"
SVC_NAME = 'telem'

URL_KEY = 'prometheus.url'
SVC_NS_KEY = 'prometheus.service_namespace'
SVC_NAME_KEY = 'prometheus.service_name'
ACCESS_TYPE_KEY = 'prometheus.access_type'

GRAFANA_URL_KEY = 'grafana.url'
GRAFANA_SVC_NS_KEY = 'grafana.service_namespace'
GRAFANA_SVC_NAME_KEY = 'grafana.service_name'
GRAFANA_ACCESS_TYPE_KEY = 'grafana.access_type'

PROTOTYPE_MODE_KTEA = KteaDict(
  type=KTEA_TYPE_SERVER,
  version="1.0.0",
  uri="https://api.nmachine.io/ktea/nmachine/prom-plugin"
)

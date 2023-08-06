import time
import traceback
from datetime import datetime, timedelta
from json import JSONDecodeError
from typing import Optional, Dict, Tuple, Any
from urllib.parse import quote

import requests
from k8kat.res.svc.kat_svc import KatSvc

from kama_prom_plugin.consts import PLUGIN_ID, GRAFANA_SVC_NAME_KEY, GRAFANA_SVC_NS_KEY, SVC_NS_KEY, SVC_NAME_KEY, \
  ACCESS_TYPE_KEY, GRAFANA_ACCESS_TYPE_KEY, URL_KEY, GRAFANA_URL_KEY
from kama_sdk.core.core.config_man import config_man
from kama_prom_plugin.models.types import PromData
from kama_sdk.utils import env_utils, utils
from kama_sdk.utils.logging import lwar


class PromClient:
  # _config: Optional[Dict]
  #
  def __init__(self, config: Optional[Dict] = None):
    # self._config = config
    pass

  def compute_vector(self, *args) -> Optional[PromData]:
    path, args = instant_path_and_args(*args)
    return self.do_invoke(path, args)

  def compute_matrix(self, *args) -> Optional[PromData]:
    path, args = gen_series_args(*args)
    return self.do_invoke(path, args)

  def do_invoke(self, path: str, url_args: Dict) -> Optional[PromData]:
    if self.is_prom_server_in_cluster():
      if svc := self.find_prom_svc():
        if env_utils.is_in_cluster():
          base_url = self.get_base_in_cluster_url()
          response = invoke_normal_url(base_url, path, url_args)
        else:
          response = invoke_proxy_url(svc, path, url_args)
      else:
        return None
    else:
      base_url = self.get_prom_ext_url()
      response = invoke_normal_url(base_url, path, url_args)

    if response:
      return response.get('data')

  def find_prom_svc(self) -> Optional[KatSvc]:
    if self.get_config():
      prom_ns = self.get_config_value(SVC_NS_KEY)
      prom_name = self.get_config_value(SVC_NAME_KEY)
      return KatSvc.find(prom_name, prom_ns)

  def find_grafana_svc(self) -> Optional[KatSvc]:
    if self.get_config():
      svc_ns = self.get_config_value(GRAFANA_SVC_NS_KEY)
      svc_name = self.get_config_value(GRAFANA_SVC_NAME_KEY)
      return KatSvc.find(svc_name, svc_ns)

  def get_config_value(self, deep_key: str) -> Optional[Any]:
    return utils.deep_get(self.get_config(), deep_key)

  def get_config(self) -> Optional[Dict]:
    return config_man.get_merged_vars(space=PLUGIN_ID)

  def is_grafana_configured(self):
    if self.is_grafana_server_in_cluster():
      return self.find_prom_svc() is not None
    else:
      return self.get_prom_ext_url()

  def is_enabled(self) -> bool:
    access_type = self.get_config_value(ACCESS_TYPE_KEY) or None
    return access_type in legal_access_types

  def is_prom_server_in_cluster(self) -> bool:
    return self.get_config_value(ACCESS_TYPE_KEY) == access_type_k8s

  def is_grafana_server_in_cluster(self) -> bool:
    return self.get_config_value(GRAFANA_ACCESS_TYPE_KEY) == access_type_k8s

  def get_base_in_cluster_url(self) -> str:
    if svc := self.find_prom_svc():
      port = svc.first_tcp_port_num()
      return f"http://{svc.name}.{svc.namespace}:{port}"

  def get_prom_ext_url(self) -> str:
    return self.get_config_value(URL_KEY)

  def get_grafana_ext_url(self) -> str:
    return self.get_config_value(GRAFANA_URL_KEY)


def instant_path_and_args(query: str, ts: datetime = None) -> Tuple:
  base = '/api/v1/query'
  ts = ts or datetime.now()
  args = {
    'query': query,
    'time': fmt_time(ts)
  }
  return base, args


def gen_series_args(query: str, step=None, t0=None, tn=None) -> Tuple:
  base = '/api/v1/query_range'
  t_start = t0 or datetime.now() - timedelta(days=7)
  t_end = tn or datetime.now()
  args = {
    'query': query,
    'start': fmt_time(t_start),
    'end': fmt_time(t_end),
    'step': step or '1h'
  }
  return base, args


def fmt_time(timestamp: datetime):
  return int(time.mktime(timestamp.timetuple()))


def invoke_proxy_url(svc: KatSvc, path: str, url_args: Dict) -> Optional[Dict]:
  resp = svc.proxy_get(path, url_args) or {}
  if resp.get('status', 500) < 300:
    try:
      body = resp.get('body')
      return body
    except Exception as e:
      lwar(f"prom decode failed for resp {resp}", exc=e)
      return None


def invoke_normal_url(base_url, path, args: Dict) -> Optional[Dict]:
  full_url = f"{base_url}{path}?{dict_args2str(args)}"
  resp = requests.get(full_url)
  if resp and resp.ok:
    try:
      return resp.json()
    except JSONDecodeError as e:
      lwar("svc resp decode", exc=e)
  return None


def dict_args2str(args: Dict) -> str:
  as_list = [f"{k}={quote(str(v))}" for k, v in list(args.items())]
  return "&".join(as_list)


def invoke_pure_http(path, args) -> Optional[Dict]:
  arg2str = lambda arg: f"{arg[0]}={arg[1]}"
  url = f"{path}?{'&'.join(list(map(arg2str, args.items())))}"
  # noinspection PyBroadException
  try:
    return requests.get(url).json()
  except:
    print(traceback.format_exc())
    print(f"[kama_sdk:prom_client] pure http invoke ^^ fail")
    return None


prom_client = PromClient()

access_type_k8s = 'kubernetes'
access_type_generic = 'generic'
legal_access_types = [access_type_k8s, access_type_generic]

from k8kat.res.svc.kat_svc import KatSvc
from werkzeug.utils import cached_property

from kama_sdk.model.supplier.base.supplier import Supplier
from kama_prom_plugin.models.prom_client import prom_client
from kama_prom_plugin.models.prom_data_supplier import PromDataSupplier


class GrafanaStateSupplier(Supplier):

  @cached_property
  def is_configured(self):
    return PromDataSupplier({}).do_ping()

  @cached_property
  def svc(self) -> KatSvc:
    return prom_client.find_grafana_svc()

  @cached_property
  def is_in_cluster(self):
    return prom_client.is_grafana_server_in_cluster()

  @cached_property
  def status(self):
    return "enabled" if self.is_configured else "disabled"

  @cached_property
  def action_preview_str(self):
    if self.is_configured:
      if self.is_in_cluster:
        return "http://localhost"
      else:
        return prom_client.get_grafana_ext_url()
    else:
      return 'no access'

  @cached_property
  def action_spec(self):
    if self.is_configured:
      return dict(
        type='port_forward',
        uri=dict(
          pod_port=self.svc.first_tcp_port_num(),
          pod_name=self.svc.name,
          namespace=self.svc.namespace,
        )
      )
    else:
      return dict(
        type='www',
        uri=prom_client.get_grafana_ext_url()
      )

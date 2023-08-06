from datetime import datetime, timedelta
from typing import Dict, Optional, Union

from kama_prom_plugin.models.prom_client import PromClient, prom_client
from kama_prom_plugin.models.types import PromMatrix, PromVector
from kama_sdk.model.base.model_decorators import model_attr
from kama_sdk.model.supplier.base.supplier import Supplier, SER_NATIVE, SERIALIZER_KEY
from kama_sdk.utils.logging import lerr


class PromDataSupplier(Supplier):

  def get_client(self) -> Optional[PromClient]:
    if config := self.get_client_config_root():
      return PromClient(config)
    else:
      return prom_client

  def get_client_config_root(self) -> Optional[Dict]:
    return self.resolve_attr_value(CLIENT_CONFIG, depth=100)

  @model_attr(cached=False)
  def get_t0(self) -> datetime:
    offset = self.get_local_attr(T0_OFFSET_KEY, backup={'hours': 3})
    return parse_from_now(offset)

  @model_attr(cached=False)
  def get_tn(self) -> datetime:
    offset = self.get_attr(TN_OFFSET_KEY, backup={'minutes': 0})
    return parse_from_now(offset)

  @model_attr(cached=False)
  def get_step(self) -> str:
    return self.get_local_attr(STEP_KEY, backup='1h')

  def get_serializer_type(self) -> str:
    return self.get_attr(SERIALIZER_KEY, backup=SER_NATIVE)

  def get_data_type(self) -> str:
    return self.get_attr(
      TYPE_KEY,
      backup='matrix',
      lookback=0
    )

  def resolve(self) -> Union[PromMatrix, PromVector]:
    data_type = self.get_data_type()

    if data_type == 'matrix':
      response = self.do_fetch_matrix()
    elif data_type == 'vector':
      response = self.do_fetch_vector()
    elif data_type == 'ping':
      response = self.do_ping()
    else:
      lerr(f"bad req type {data_type}", sig=self.sig())
      response = None

    return response

  def do_fetch_matrix(self) -> Optional[PromMatrix]:
    prom_data = self.get_client().compute_matrix(
      self.get_source_data(),
      self.get_step(),
      self.get_t0(),
      self.get_tn()
    )
    # print("RAW")
    # print(prom_data)
    return prom_data['result'] if prom_data else None

  def do_ping(self) -> bool:
    try:
      response = self.get_client().compute_vector("up")
      return response is not None
    except:
      return False

  def do_fetch_vector(self) -> Optional[PromVector]:
    prom_data = self.get_client().compute_vector(
      self.get_source_data(),
      self.get_tn()
    )
    return prom_data['result'] if prom_data else None

def parse_from_now(expr: Dict) -> datetime:
  difference = {k: int(v) for k, v in expr.items()}
  return datetime.now() - timedelta(**difference)


TYPE_KEY = 'type'
STEP_KEY = 'step'
T0_OFFSET_KEY = 't0_offset'
TN_OFFSET_KEY = 'tn_offset'
CLIENT_CONFIG = 'client_config'

from kama_prom_plugin import plugin
from kama_prom_plugin.consts import PLUGIN_ID
from kama_prom_plugin.models.prom_client import ACCESS_TYPE_KEY, SVC_NS_KEY, SVC_NAME_KEY
from kama_sdk.core.core.config_man import config_man
from kama_sdk.model.base.mc import KIND_KEY
from kama_prom_plugin.models import prom_client as client_module
from kama_prom_plugin.models import prom_data_supplier as supplier_module
from kama_prom_plugin.models.prom_data_supplier import PromDataSupplier
from kama_sdk.model.base.models_manager import models_manager
from kama_sdk.model.supplier.base.supplier import SRC_DATA_KEY


def vanilla_setup():
  config_man.patch_user_vars({
    ACCESS_TYPE_KEY: client_module.access_type_k8s,
    SVC_NS_KEY: REQUIRED_SVC_NS,
    SVC_NAME_KEY: REQUIRED_SVC_NAME
  }, space=PLUGIN_ID)


def create_simple_matrix_supplier() -> PromDataSupplier:
  return PromDataSupplier.inflate({
    KIND_KEY: PromDataSupplier.__name__,
    supplier_module.TYPE_KEY: 'matrix',
    supplier_module.STEP_KEY: '15m',
    SRC_DATA_KEY: "container_memory_usage_bytes{namespace=\"monitoring\"}"
  })


def easy_setup():
  vanilla_setup()
  descriptors = plugin.gather_model_descriptors()
  models_manager.add_models(plugin.gather_custom_models())
  models_manager.add_any_descriptors(descriptors, space=PLUGIN_ID)


REQUIRED_SVC_NS = 'monitoring'
REQUIRED_SVC_NAME = 'monitoring-prometheus-server'

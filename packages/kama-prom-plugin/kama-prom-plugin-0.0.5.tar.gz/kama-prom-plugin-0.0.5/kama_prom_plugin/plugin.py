import os
from typing import List, Dict, Type

from kama_prom_plugin.consts import PLUGIN_ID, PROTOTYPE_MODE_KTEA
from kama_sdk.core.core.plugin_type_defs import PluginManifest
from kama_sdk.model.base.model import Model
from kama_prom_plugin.models.grafana_state_supplier import GrafanaStateSupplier
from kama_prom_plugin.models.prom_data_supplier import PromDataSupplier
from kama_prom_plugin.models.prom_matrix_to_timeseries_supplier import PromMatrixToSeriesSupplier
from kama_prom_plugin.models.prom_state_supplier import PromStateSupplier
from kama_prom_plugin.models.prom_vector_to_groups_provider import PromVectorsToGroupsSupplier
from kama_sdk.utils.descriptor_utils import load_dir_yamls


def get_manifest():
  return PluginManifest(
    id=PLUGIN_ID,
    publisher_identifier='nmachine',
    app_identifier='prom-plugin',
    model_descriptors=gather_model_descriptors(),
    asset_paths=[assets_path],
    model_classes=gather_custom_models(),
    virtual_kteas=[],
    prototype_mode_ktea=PROTOTYPE_MODE_KTEA
  )

def gather_custom_models() -> List[Type[Model]]:
  return [
    PromDataSupplier,
    PromMatrixToSeriesSupplier,
    PromVectorsToGroupsSupplier,
    PromStateSupplier,
    GrafanaStateSupplier
  ]

def gather_model_descriptors() -> List[Dict]:
  return load_dir_yamls(descriptors_path, recursive=True)


root_dir = os.path.dirname(os.path.abspath(__file__))
descriptors_path = f'{root_dir}/descriptors'
assets_path = f'{root_dir}/assets'

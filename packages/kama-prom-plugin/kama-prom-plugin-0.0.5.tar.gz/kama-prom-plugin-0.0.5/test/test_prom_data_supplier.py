from kama_sdk.model.base.mc import KIND_KEY
from kama_sdk.model.supplier.base.supplier import SRC_DATA_KEY
from test import prom_test_helper as my_helper
from kama_sdk.utils.unittest.base_classes import ClusterTest
from kama_prom_plugin.models.prom_data_supplier import PromDataSupplier
from kama_prom_plugin.models import prom_data_supplier as supplier_module
from test.prom_test_helper import easy_setup


class TestPromDataSupplier(ClusterTest):

  def setUp(self) -> None:
    super(TestPromDataSupplier, self).setUp()
    easy_setup()

  def test_resolve_custom_client_config(self):
    supplier = PromDataSupplier.inflate({
      supplier_module.TYPE_KEY: 'ping',
      supplier_module.CLIENT_CONFIG: {}
    })
    self.assertTrue(supplier.resolve())

  def test_foo(self):
    inst = PromDataSupplier.inflate({
      KIND_KEY: PromDataSupplier.__name__,
      supplier_module.TYPE_KEY: 'vector',
      supplier_module.STEP_KEY: '15m',
      SRC_DATA_KEY: group_query
    })
    result = inst.resolve()
    self.assertIsNotNone(result)

  def test_supply_matrix(self):
    supplier = my_helper.create_simple_matrix_supplier()
    result = supplier.resolve()
    self.assertIsNotNone(result)
    self.assertGreater(len(result), 15)
    self.assertGreater(len(result[0].items()), 1)


group_query = "sum(" \
                "container_memory_usage_bytes{" \
                " container_name!='POD', " \
                " image!=''" \
                "}" \
              ") by(namespace)"

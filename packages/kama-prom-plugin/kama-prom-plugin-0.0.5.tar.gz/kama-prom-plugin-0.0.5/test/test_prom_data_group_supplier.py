from kama_sdk.utils.unittest.base_classes import ClusterTest
from kama_prom_plugin.models.prom_vector_to_groups_provider import PromVectorsToGroupsSupplier


class TestPromDataGroupSupplier(ClusterTest):
  
  def test_compute(self):
    computer = PromVectorsToGroupsSupplier.inflate({
      'source': data
    })
    self.assertEqual(expect, computer.resolve())


data = [
  {'metric': {'namespace': 'cert-manager'}, 'value': [1624109003, '80175104']},
  {'metric': {'namespace': 'ktea-servers'}, 'value': [1624109003, '196411392']}, 
  {'metric': {'namespace': 'monitoring'}, 'value': [1624109003, '722571264']}
]


expect = [
  {'name': 'cert-manager', 'value': 80175104.0},
  {'name': 'ktea-servers', 'value': 196411392.0},
  {'name': 'monitoring', 'value': 722571264.0}
]

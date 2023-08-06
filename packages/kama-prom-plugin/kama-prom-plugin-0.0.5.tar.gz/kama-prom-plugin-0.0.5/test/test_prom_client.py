from kama_prom_plugin.consts import SVC_NS_KEY
from kama_sdk.utils.unittest.base_classes import ClusterTest
from kama_prom_plugin.models.prom_client import prom_client
from test.prom_test_helper import easy_setup, REQUIRED_SVC_NS, REQUIRED_SVC_NAME


class TestPromClient(ClusterTest):

  def setUp(self) -> None:
    super(TestPromClient, self).setUp()
    easy_setup()

  def test_get_config(self):
    actual = prom_client.get_config()
    self.assertEqual(expected_config, actual)

  def test_connection(self):
    svc = prom_client.find_prom_svc()
    self.assertIsNotNone(svc)
    self.assertEqual(REQUIRED_SVC_NS, svc.namespace)
    self.assertEqual(REQUIRED_SVC_NAME, svc.name)
    self.assertTrue(prom_client.is_prom_server_in_cluster())

  def test_invoke(self):
      resp = prom_client.compute_vector('up')
      self.assertEqual('vector', resp['resultType'])


expected_config = {
  'prometheus': {
    'access_type': 'kubernetes',
    'service_namespace': REQUIRED_SVC_NS,
    'service_name': REQUIRED_SVC_NAME
  }
}

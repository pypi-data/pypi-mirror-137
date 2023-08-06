from kama_prom_plugin.models.prom_matrix_to_timeseries_supplier import PromMatrixToSeriesSupplier
from kama_sdk.utils.unittest.base_classes import ClusterTest
from kama_prom_plugin.models.types import PromMatrix
from test import prom_test_helper as my_helper


class TestPromMatrixToSeriesSupplier(ClusterTest):

  def test_convert_implicit_keys(self):
    actual = subject().matrix2series(prom_matrix_implicit_keys)
    self.assertEqual(expected_implicit, actual)

  def test_convert_explicit_keys(self):
    actual = subject().matrix2series(prom_matrix_explicit_keys)
    self.assertEqual(expected_explicit, actual)

  def test_with_real_data_source(self):
    if my_helper.easy_setup():
      config = my_helper.create_simple_matrix_supplier().get_config
      result = subject(source=config).resolve()
      self.assertIsNotNone(result)
      self.assertGreater(len(result), 0)


def subject(**kwargs):
  return PromMatrixToSeriesSupplier.inflate(kwargs)


t0 = 1615803913

t1 = 1615807513

prom_matrix_implicit_keys: PromMatrix = [
  {
    "metric": {},
    'values': [[t0, "1"], [t1, "2"]]
  }
]

prom_matrix_explicit_keys: PromMatrix = [
  {
    "metric": {'foo': 'bar'},
    'values': [[t0, "1"], [t1, "2"]]
  },
  {
    "metric": {'foo': 'baz'},
    'values': [[t0, "3"], [t1, "4"]]
  },
  {
    "metric": {},
    'values': [[t0, "5"], [t1, "6"]]
  }
]


expected_implicit = [
  {'value': 1, 'timestamp': '2021-03-15 10:25:13'},
  {'value': 2, 'timestamp': '2021-03-15 11:25:13'}
]


expected_explicit = [
  {'bar': 1, 'baz': 3, 'value': 5, 'timestamp': '2021-03-15 10:25:13'},
  {'bar': 2, 'baz': 4, 'value': 6, 'timestamp': '2021-03-15 11:25:13'}
]

from datetime import datetime
from typing import Dict, List, Optional

from kama_prom_plugin.models.types import PromMatrixEntry
from kama_sdk.model.supplier.base.supplier import Supplier
from kama_sdk.utils.logging import lwar


class PromMatrixToSeriesSupplier(Supplier):

  def source_data(self) -> List[PromMatrixEntry]:
    return super(PromMatrixToSeriesSupplier, self).get_source_data()

  def _compute(self) -> Optional[List]:
    if data := self.source_data():
      as_time_series = self.matrix2series(data)
      return as_time_series
    else:
      return None

  @staticmethod
  def matrix2series(matrix_entries: List[PromMatrixEntry]) -> List:
    output = []
    # warn_agg_series(matrix_entries)
    for matrix_entry in matrix_entries:
      key = infer_series_key(matrix_entry['metric'])
      for datapoint in matrix_entry['values']:
        if len(datapoint) == 2:
          epoch, computed_val = datapoint
          entry = find_or_create_entry(output, epoch)
          entry[key] = float(computed_val)
        else:
          print(f"[kama_sdk:prom_series_computer] !=2 entry val {datapoint}")

    for datapoint in output:
      epoch = datapoint['epoch']
      del datapoint['epoch']
      datapoint['timestamp'] = str(datetime.fromtimestamp(epoch))

    return output


def infer_series_key(metric: Dict) -> str:
  as_items = list(metric.items())
  if len(as_items) == 1:
    return as_items[0][1]
  elif len(as_items) == 0:
    return 'value'
  else:
    lwar(f"can't handle n-dim metric {metric}")
    return 'value'


def subserie_for_metric(subseries: List, metric_key: str) -> List:
  if metric_key == 'value':
    if len(subseries) == 1:
      return subseries[0]
    else:
      print("DANGER key is 'value' but +1 metric types!")
      return []

  for sub_series in subseries:
    if len(sub_series['metric']) > 0:
      if sub_series['metric'].values()[0] == metric_key:
        return sub_series
    elif len(sub_series['metric']) == 0:
      return sub_series

  print(f"DANGER no subseries for {metric_key}")
  return []


# def warn_agg_series(query_result: List[Dict]):
#   pass
# metric_key_sets = [set(g['metric'].keys()) for g in query_result]
# if len(metric_key_sets) >= 2:
#   for i in range(len(metric_key_sets)):
#     pass


def find_or_create_entry(output: List, epoch: int) -> Dict:
  for datapoint in output:
    if datapoint['epoch'] == epoch:
      return datapoint

  datapoint = {'epoch': epoch}
  output.append(datapoint)
  return datapoint


HUMANIZER_KEY = 'humanizer'
APPEND_UNIT = 'with_unit'

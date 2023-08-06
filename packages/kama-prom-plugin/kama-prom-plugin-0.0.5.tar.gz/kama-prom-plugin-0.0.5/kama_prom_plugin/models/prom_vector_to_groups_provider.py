from typing import Any, List

from kama_prom_plugin.models.types import PromVectorEntry
from kama_sdk.model.supplier.base.supplier import Supplier


class PromVectorsToGroupsSupplier(Supplier):

  def get_source_data(self) -> List[PromVectorEntry]:
    return super(PromVectorsToGroupsSupplier, self).get_source_data()

  def _compute(self) -> Any:
    if data := self.get_source_data():
      grouped = self.vector2groups(data)
      return grouped
    else:
      return None

  @staticmethod
  def vector2groups(vectors: List[PromVectorEntry]):
    result = []
    for i, vector in list(enumerate(vectors)):
      metric = vector.get('metric')
      value = vector.get('value')

      is_easy_label = isinstance(metric, dict) and len(metric) > 0
      is_easy_value = isinstance(value, list) and len(value) > 1

      metric_name = list(metric.values())[0] if is_easy_label else None
      num_value = value[1] if is_easy_value else None

      result.append({
        'name': metric_name or f"group {i + 1}",
        'value': float(num_value)
      })

    return result

from typing import Dict, List, Union

from typing_extensions import TypedDict


class PromMatrixEntry(TypedDict):
  metric: Dict
  values: List[Union[str, int]]


class PromVectorEntry(TypedDict):
  metric: Dict
  value: List[Union[str, int]]


PromMatrix = List[PromMatrixEntry]


PromVector = List[PromVectorEntry]


class PromData(TypedDict):
  resultType: Dict
  result: Union[PromMatrix, PromVector]

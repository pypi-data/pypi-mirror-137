from typing import Any

from kama_sdk.model.humanizer.quantity_humanizer import QuantityHumanizer


def process_num(computed_val: Any, humanizer: QuantityHumanizer, with_unit: bool):
  try:
    decimal_value = float(computed_val)
    if humanizer:
      if with_unit:
        return humanizer.humanize_expr(decimal_value)
      else:
        return humanizer.humanize_quantity(decimal_value)
    else:
      return decimal_value
  except:
    return 0

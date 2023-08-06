def _remove_none_values(d: dict):
  return {k: v for k, v in d.items() if v is not None}

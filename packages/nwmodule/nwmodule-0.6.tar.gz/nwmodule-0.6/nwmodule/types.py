from typing import Callable, Dict, Any
import torch as tr

# loss(y, gt, **kargs) -> float
CriterionType = Callable[[tr.Tensor, tr.Tensor, dict], float]
MetricType = CriterionType
# {"callback": {potential: any_results}}
EpochResultsType = Dict[str, Any]
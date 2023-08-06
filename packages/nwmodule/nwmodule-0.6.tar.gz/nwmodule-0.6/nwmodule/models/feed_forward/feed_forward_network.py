from overrides import overrides
from typing import Any, Optional, Dict
import torch as tr

from .feed_forward_trainer import FeedForwardTrainer
from ...logger import logger
from ...nwmodule import NWModule
from ...types import CriterionType

# Wrapper on top of the PyTorch model. Added methods for saving and loading a state. To completly implement a PyTorch
#  model, one must define layers in the object's constructor, call setOptimizer, setCriterion and implement the
#  forward method identically like a normal PyTorch model.
class FeedForwardNetwork(NWModule):
    def __init__(self, hyperParameters: Optional[Dict]=None):
        super().__init__(hyperParameters)
        self._criterion_fn = None

    @overrides
    def train_step(self, x: Any, **kwargs) -> Any:
        return self.forward(x, **kwargs)

    @overrides
    def inference_step(self, x: Any, **kwargs) -> Any:
        return self.forward(x, **kwargs)

    @overrides
    def criterion(self, y: Any, gt: Any) -> tr.Tensor:
        return self.criterion_fn(y, gt)

    @overrides
    def get_trainer_type(self) -> type:
        return FeedForwardTrainer

    @property
    def criterion_fn(self):
        assert self._criterion_fn is not None
        return self._criterion_fn
    
    @criterion_fn.setter
    def criterion_fn(self, _criterion_fn: CriterionType):
        assert isinstance(_criterion_fn, CriterionType)
        self._criterion_fn = _criterion_fn

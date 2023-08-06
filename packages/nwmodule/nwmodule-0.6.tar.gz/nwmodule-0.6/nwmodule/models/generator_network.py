from overrides import overrides
from typing import Any
import torch as tr
from .feed_forward import FeedForwardNetwork

class GeneratorNetwork(FeedForwardNetwork):
    def __init__(self, noise_size: int, **kwargs):
        super().__init__(**kwargs)
        self.noise_size = noise_size

    @overrides
    def inference_step(self, x: Any, **kwargs) -> Any:
        assert isinstance(x, int), type(x)
        noise = tr.randn(x, self.noise_size).to(self.getDevice())
        return self.forward(noise)

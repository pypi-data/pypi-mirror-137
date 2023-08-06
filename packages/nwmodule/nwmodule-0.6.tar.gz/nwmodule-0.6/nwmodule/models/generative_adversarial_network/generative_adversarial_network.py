import torch as tr
import torch.optim as optim
from overrides import overrides
from typing import List, Any

from .gan_trainer import GANTrainer
from ...nwmodule import NWModule
from ...metrics import MetricWrapper, Metric
from ..generator_network import GeneratorNetwork

class GANOptimizer(optim.Optimizer):
    def __init__(self, model, optimizer, **kwargs):
        self.model = model
        model.generator.setOptimizer(optimizer, **kwargs)
        model.discriminator.setOptimizer(optimizer, **kwargs)

    def state_dict(self):
        return {
            "discriminator" : self.model.discriminator.getOptimizer().state_dict(),
            "generator" : self.model.generator.getOptimizer().state_dict()
        }

    def load_state_dict(self, state):
        self.model.discriminator.getOptimizer().load_state_dict(state["discriminator"])
        self.model.generator.getOptimizer().load_state_dict(state["generator"])

    @overrides
    def step(self, closure=None):
        self.model.discriminator.getOptimizer().step(closure)
        self.model.generator.getOptimizer().step(closure)

    @overrides
    def __str__(self):
        Str = "[Gan Optimizer]"
        Str += f"\n - Generator: {self.model.generator.getOptimizerStr()}"
        Str += f"\n - Discriminator: {self.model.discriminator.getOptimizerStr()}" 
        return Str

    def __getattr__(self, key):
        assert key in ("discriminator", "generator", "param_groups")
        if key == "param_groups":
            for pg in self.model.generator.getOptimizer().param_groups:
                yield pg
            for pg in self.model.discriminator.getOptimizer().param_groups:
                yield pg
        else:
            return self.state_dict()[key]

class GenerativeAdversarialNetwork(NWModule):
    def __init__(self, generator: GeneratorNetwork, discriminator: NWModule):
        super().__init__()
        assert isinstance(generator, GeneratorNetwork)
        self.generator = generator
        self.discriminator = discriminator

    @overrides
    def get_default_metrics(self) -> List[Metric]:
        default = super().get_default_metrics()
        gan_metrics = [
            MetricWrapper("Generator Loss", lambda y, _: y["gLoss"], "min"),
            MetricWrapper("Discriminator Loss", lambda y, _: y["dLoss"], "min"),
        ]
        return [*default, *gan_metrics]

    @overrides
    def setOptimizer(self, optimizer, **kwargs):
        assert not isinstance(optimizer, optim.Optimizer)
        ganOptimizer = GANOptimizer(self, optimizer, **kwargs)
        super().setOptimizer(ganOptimizer, **kwargs)

    @overrides
    def train_step(self, x: Any, **kwargs) -> Any:
        assert False

    @overrides
    def criterion(self, y, gt) -> tr.Tensor:
        assert False

    @overrides
    def inference_step(self, x: Any, **kwargs) -> Any:
        return self.generator.inference_step(x, **kwargs)

    @overrides
    def get_trainer_type(self) -> type:
        return GANTrainer

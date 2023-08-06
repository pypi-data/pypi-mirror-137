import numpy as np
from overrides import overrides
from .metric import Metric

class Loss(Metric):
    def __init__(self):
        super().__init__(name="Loss", direction="min")

    def __call__(self, results:np.ndarray, labels:np.ndarray, **kwargs):
        return kwargs["loss"]

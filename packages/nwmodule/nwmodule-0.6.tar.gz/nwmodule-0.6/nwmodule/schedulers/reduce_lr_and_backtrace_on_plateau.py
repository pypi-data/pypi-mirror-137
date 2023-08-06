from torch.optim.lr_scheduler import _LRScheduler
from overrides import overrides
from copy import deepcopy
from ..nwmodule import NWModule
from ..logger import logger

class ReduceLRAndBacktrackOnPlateau(_LRScheduler):
    def __init__(self, model: NWModule, metric_name: str, patience: int, factor: float):
        assert patience > 0
        self.model = model
        self.metric_name = metric_name
        self.patience = patience
        self.factor = factor

        self.lastRelevantWeights = self.model.serializer.doSaveWeights()
        self.lastRelevantOptimizer = self.model.getOptimizer().state_dict()
        self.currentLR = [float(pg["lr"]) for pg in self.model.getOptimizer().param_groups]
        self.metric = self.model.getMetric(self.metric_name)
        self.numBadInARow = 0
        metricExtremes = self.metric.getExtremes()
        self.lastRelevantValue = metricExtremes["min"] if self.metric.direction == "max" else metricExtremes["max"]
        self.storedArgs = None

    def state_dict(self):
        return {
            "lastRelevantWeights" : self.lastRelevantWeights,
            "metric_name" : self.metric_name,
            "numBadInARow" : self.numBadInARow,
            "lastRelevantValue" : self.lastRelevantValue,
            "currentLR" : self.currentLR
        }

    def load_state_dict(self, state_dict):
        self.lastRelevantWeights = state_dict["lastRelevantWeights"]
        self.metric_name = state_dict["metric_name"]
        self.metric = self.model.getMetric(self.metric_name)
        self.numBadInARow = state_dict["numBadInARow"]
        self.lastRelevantValue = state_dict["lastRelevantValue"]
        self.currentLR = state_dict["currentLR"]

    @overrides
    def step(self, epoch=None):
        history = self.model.trainHistory[-1]
        key = "Validation" if "Validation" in history and not history["Validation"] is None else "Train"
        score = history[key][self.metric_name]

        if not self.metric.compareFunction(score, self.lastRelevantValue):
            self.numBadInARow += 1
        else:
            self.lastRelevantValue = score
            self.numBadInARow = 0
            self.lastRelevantWeights = deepcopy(self.model.serializer.doSaveWeights())
            self.lastRelevantOptimizer = deepcopy(self.model.getOptimizer().state_dict())

        if self.numBadInARow == self.patience:
            logger.debug(f"Reached {self.numBadInARow} bad epochs. Resetting to last good checkpoint. "
                         f"Old LR: {self.currentLR[0]:.5f}. New LR: {self.currentLR[0] / self.factor:.5f}")
            self.numBadInARow = 0
            self.model.serializer.doLoadWeights(self.lastRelevantWeights)
            self.model.getOptimizer().load_state_dict(self.lastRelevantOptimizer)
            for i, param_group in enumerate(self.model.getOptimizer().param_groups):
                self.currentLR[i] /= self.factor
                param_group["lr"] = self.currentLR[i]

    def __str__(self):
        return "ReduceLRAndBacktrackOnPlateau (Patience: %d. Factor: %2.2f)" % (self.patience, self.factor)

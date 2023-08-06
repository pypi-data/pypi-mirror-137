import torch as tr
import numpy as np
from pathlib import Path
from overrides import overrides
from typing import Any
from .callback import Callback
from ..logger import logger
from ..types import EpochResultsType

# TODO: Remove mode from ctor and infer at epoch end.
class EarlyStopping(Callback):
    def __init__(self, metric_name: str="Loss", min_delta: float=0, patience: float=10, percentage: bool=False):
        self.metric_name = metric_name
        self.min_delta = min_delta
        self.patience = patience
        self.percentage = percentage
        super().__init__(name=str(self))

        self.bestMetricScore = None
        self.numBadEpochs = 0
        self.metricDirection = None

    @overrides
    def on_epoch_start(self, model, working_directory: Path):
        pass

    @overrides
    def on_iteration_start(self, **kwargs):
        pass

    @overrides
    def on_iteration_end(self, y: tr.Tensor, gt: tr.Tensor, **kwargs) -> Any:
        pass

    @overrides
    def on_epoch_end(self, model, epoch_results: EpochResultsType, working_directory: Path) -> Any:
        if not "Train" in epoch_results or len(model.getTrainHistory()) == 0:
            return
        Key = "Validation" if "Validation" in epoch_results else "Train"
        score = epoch_results[Key][self.metric_name]
        assert not np.isnan(score)

        # First epoch we need to get some value running.
        if self.bestMetricScore is None:
            assert hasattr(model, "finished")
            self.numBadEpochs = 0
            self.bestMetricScore = score
            self.metricDirection = model.getMetric(self.metric_name).direction
            return

        fIsBetter = EarlyStopping._init_is_better(self.metricDirection, self.patience, self.percentage, self.min_delta)
        if fIsBetter(score, self.bestMetricScore):
            self.numBadEpochs = 0
            self.bestMetricScore = score
        else:
            self.numBadEpochs += 1
            logger.debug(f"Early Stopping is being applied. Num bad in a row: {self.numBadEpochs}. "
                         f"Patience: {self.patience}")

        if self.numBadEpochs >= self.patience:
            logger.debug(f"Num bad epochs in a row: {self.numBadEpochs}. Stopping the training!")
            model.finished = True

    @staticmethod
    def _init_is_better(metricDirection, patience, modePercentage, minDelta):
        if patience == 0:
            return lambda a, best: True
        fDirection = lambda a, b, c : (a < b - c if metricDirection == "min" else a > b + c)
        if modePercentage:
            return lambda a, best: fDirection(a, best, best * minDelta / 100)
        return lambda a, best : fDirection(a, best, minDelta)

    def __str__(self):
        return f"EarlyStopping (Metric: {self.metric_name}. Min delta: {self.min_delta:.2f}. " \
               f"Patience: {self.patience}. Percentage: {self.percentage})"

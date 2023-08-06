from typing import Any
from overrides import overrides
import torch as tr
from pathlib import Path

from .callback import Callback
from ..logger import logger
from ..types import EpochResultsType

# TODO: add format to saving files
# Note: This callback should be called after all (relevant) callbacks were called, otherwise we risk of storing a model
#  that hasn't updated all it's callbacks. This is relevant, for example in EarlyStopping, where we'd save the state
#  of the N-1th epoch instead of last, causing it to lead to different behavioiur pre/post loading.
class SaveModels(Callback):
    def __init__(self, mode: str, metric_name: str, **kwargs):
        assert mode in ("all", "improvements", "last", "best")
        self.mode = mode
        if isinstance(metric_name, Callback):
            metric_name = metric_name.getName()
        self.metric_name = metric_name
        self.best = None
        super().__init__(name=str(self), **kwargs)

    def saveImprovements(self, model, metric, score, epoch, workingDirectory):
        if self.best is None:
            extremes = metric.getExtremes()
            self.best = {
                "max" : extremes["min"],
                "min" : extremes["max"]
            }[metric.direction]

        compareResult = metric.compareFunction(score, self.best)
        if compareResult == False:
            logger.debug(f"Epoch {epoch}. "
                         f"Metric '{self.metric_name}' did not improve best score {self.best} with {score}")
            return

        logger.debug(f"Epoch {epoch}. Metric '{self.metric_name}' improved best score from {self.best} to {score}")
        self.best = score
        model.saveModel(workingDirectory / f"model_improvement_{self.metric_name}_epoch-{epoch}_score-{score}")

    def saveBest(self, model, metric, score, epoch, workingDirectory):
        if self.best is None:
            extremes = metric.getExtremes()
            self.best = {
                "max" : extremes["min"],
                "min" : extremes["max"]
            }[metric.direction]

        compareResult = metric.compareFunction(score, self.best)
        if compareResult == False:
            logger.debug(f"Epoch {epoch}. "
                         f"Metric '{self.metric_name}' did not improve best score {self.best} with {score}")
            return

        logger.debug(f"Epoch {epoch}. Metric '{self.metric_name}' improved best score from {self.best} to {score}")
        self.best = score
        model.saveModel(workingDirectory / f"model_best_{self.metric_name}.pkl")

    def saveLast(self, model, metric, score, epoch, workingDirectory):
        model.saveModel(workingDirectory / "model_last.pkl")
        logger.debug(f"Epoch {epoch}. Saved last model.")

    # Saving by best train loss is validation is not available, otherwise validation. Nasty situation can occur if one
    #  epoch there is a validation loss and the next one there isn't, so we need formats to avoid this and error out
    #  nicely if the format asks for validation loss and there's not validation metric reported.
    @overrides
    def on_epoch_end(self, model, epoch_results: EpochResultsType, working_directory: Path) -> Any:
        if not "Train" in epoch_results and not "Validation" in epoch_results:
            return
        epochResults = epoch_results["Validation"] if "Validation" in epoch_results else epoch_results["Train"]
        epoch = len(model.getTrainHistory())
        metric = model.getMetric(self.metric_name)
        score = epochResults[metric.name]
        score = score.mean() if isinstance(score, tr.Tensor) else score

        f = {
            "improvements" : self.saveImprovements,
            "best" : self.saveBest,
            "last" : self.saveLast
        }[self.mode]
        f(model, metric, score, epoch, working_directory)

    @overrides
    def on_epoch_start(self, model, working_directory: Path):
        assert self.metric_name in model.getMetrics(), \
            f"Metric '{self.metric_name}' not in model metrics: {list(model.getMetrics())}"

    @overrides
    def on_iteration_start(self, **kwargs):
        pass

    @overrides
    def on_iteration_end(self, y: tr.Tensor, gt: tr.Tensor, **kwargs) -> Any:
        pass

    @overrides
    def onCallbackLoad(self, additional, **kwargs):
        pass

    @overrides
    def onCallbackSave(self, **kwargs):
        pass

    @overrides
    def __str__(self):
        return f"SaveModels (Metric: {self.metric_name}. Mode: {self.mode})"

from overrides import overrides
from copy import deepcopy
from typing import List, Any, Dict
import numpy as np
import torch as tr
import matplotlib.pyplot as plt
from nwutils.dict import deepDictGet
from pathlib import Path

from .callback import Callback
from ..types import EpochResultsType

def plotModelMetricHistory(model, metric_name: str, trainHistory: Dict, workingDirectory: Path):
    metric = model.getMetric(metric_name)
    num_epochs = len(trainHistory)
    hasValidation = "Validation" in trainHistory[0]

    trainScores = [deepDictGet(epochHistory["Train"], metric_name) for epochHistory in trainHistory]
    trainScores = [x.mean() for x in trainScores] if isinstance(trainScores[0], np.ndarray) else trainScores
    trainScores = np.array(trainScores)
    valScores = None
    if hasValidation:
        valScores = [deepDictGet(epochHistory["Validation"], metric_name) for epochHistory in trainHistory]
        valScores = [x.mean() for x in valScores] if isinstance(valScores[0], np.ndarray) else valScores
        valScores = np.array(valScores)

    X = np.arange(1, num_epochs + 1)
    plt.gcf().clf()
    plt.gca().cla()
    plt.plot(X, trainScores, label=f"Train {metric_name}")

    if hasValidation:
        plt.plot(X, valScores, label=f"Val {metric_name}")
        usedValues = valScores
    else:
        usedValues = trainScores

    # Against NaNs killing the training for low data count.
    allValues = np.concatenate([usedValues, trainScores])
    Median = np.median(allValues[np.isfinite(allValues)])
    trainScores[~np.isfinite(trainScores)] = Median
    usedValues[~np.isfinite(usedValues)] = Median
    allValues[~np.isfinite(allValues)] = Median

    # assert plotBestBullet in ("none", "min", "max"), "%s" % plotBestBullet
    if metric.direction == "min":
        minX, minValue = np.argmin(usedValues), np.min(usedValues)
        plt.annotate(f"Epoch {minX + 1}\nMin {minValue:.2f}", xy=(minX + 1, minValue))
        plt.plot([minX + 1], [minValue], "o")
    elif metric.direction == "max":
        maxX, maxValue = np.argmax(usedValues), np.max(usedValues)
        plt.annotate(f"Epoch {maxX + 1}\nMax {maxValue:.2f}", xy=(maxX + 1, maxValue))
        plt.plot([maxX + 1], [maxValue], "o")
    else:
        assert False, f"Unknown direction for metric {metric}: {metric.direction}"

    # Set the y axis to have some space above and below the plot min/max values so it looks prettier.
    minValue, maxValue = np.min(allValues), np.max(allValues)
    diff = (maxValue - minValue) / 10
    plt.gca().set_ylim(minValue - diff, maxValue + diff)

    # Finally, save the figure with the name of the metric
    plt.xlabel("Epoch")
    plt.ylabel(metric_name)
    plt.legend()
    plt.savefig(f"{workingDirectory}/{metric_name}.png", dpi=120)

class PlotMetrics(Callback):
    def __init__(self, metric_names: List[str], **kwargs):
        assert len(metric_names) > 0, "Expected a list of at least one metric which will be plotted."
        self.metric_names = []
        for metric_name in metric_names:
            if isinstance(metric_name, Callback):
                metric_name = metric_name
            self.metric_names.append(metric_name)
        super().__init__(name=str(self), **kwargs)

    @overrides
    def on_epoch_end(self, model, epoch_results: EpochResultsType, working_directory: Path) -> Any:
        if not "Train" in epoch_results or len(model.getTrainHistory()) == 0:
            return

        history = deepcopy(model.getTrainHistory())
        history.append(epoch_results)
        for i in range(len(self.metric_names)):
            plotModelMetricHistory(model, self.metric_names[i], history, working_directory)

    @overrides
    def on_epoch_start(self, model, working_directory: Path):
        for metric_name in self.metric_names:
            assert metric_name in model.getMetrics(), \
                f"Metric '{metric_name}' not in model metrics: {list(model.getMetrics())}"

    @overrides
    def on_iteration_start(self, **kwargs):
        pass

    @overrides
    def on_iteration_end(self, y: tr.Tensor, gt: tr.Tensor, **kwargs) -> Any:
        pass

    @overrides
    def onCallbackSave(self, **kwargs):
        self.directions = None

    @overrides
    def onCallbackLoad(self, additional, **kwargs):
        pass

    @overrides
    def __str__(self):
        assert len(self.metric_names) >= 1
        Str = str(self.metric_names[0])
        for i in range(len(self.metric_names)):
            Str += f", {self.metric_names[i]}"
        return f"PlotMetrics ({Str})"

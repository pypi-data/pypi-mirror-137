from __future__ import annotations
import torch as tr
from abc import abstractmethod
from typing import Dict, Any
from pathlib import Path
from overrides import overrides

from ..types import EpochResultsType
from ..callbacks import Callback

# @brief Base Class for all metrics. It defines a direction, which represents whether the metric is minimized or
#  maximized.
class Metric(Callback):
    # @param[in] direction Defines the "direction" of the metric, as in if the better value means it is minimized or
    #  maximized. For example, Loss functions (or errors in general) are minimized, thus "min". However, other metrics
    #  such as Accuracy or F1Score are to be maximized, hence "max". Defaults to "min".
    def __init__(self, name: str, direction: str="min"):
        super().__init__(name)
        assert direction in ("min", "max")
        self.direction = direction

    # @brief The default value of the metric, used by some implementations to define defaults for various statistics
    # @return A value that represents the default value of the metric
    def defaultValue(self) -> float:
        return 0.0

    def getExtremes(self) -> Dict[str, float]:
        return {"min": -tr.inf, "max": tr.inf}

    # @brief Provides a sane way of comparing two results of this metric
    # @return Returns a callback that can compare two results and returns a bool value. Returns true if
    #  - for direction == "max", a > b
    #  - for direciton == "min", a < b
    def compareFunction(self, a: float, b: float) -> bool:
        return {
            "min": a < b,
            "max": a > b,
        }[self.direction]

    @overrides
    def on_epoch_start(self, model, working_directory: Path):
        pass

    @overrides
    def on_epoch_end(self, model, epoch_results: EpochResultsType, working_directory: Path) -> Any:
        pass  

    @overrides
    def on_iteration_start(self, **kwargs):
        pass

    @overrides
    def on_iteration_end(self, y: tr.Tensor, gt: tr.Tensor, **kwargs) -> Any:
        return self.__call__(y, gt, **kwargs)

    @overrides
    def onCallbackLoad(self, additional, **kwargs):
        pass

    @overrides
    def onCallbackSave(self, **kwargs):
        pass

    # @brief The main method that must be implemented by a metric
    @abstractmethod
    def __call__(self, y: tr.Tensor, gt: tr.Tensor, **kwargs):
        pass

    def __eq__(self, other: Union[Callback, str]) -> bool: # type: ignore[override]
        this_name = self.name
        other_name = other
        if isinstance(other, Callback):
            other_name = other_name.name
        assert isinstance(other_name, str), type(other_name)
        return this_name == other_name # type: ignore

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return str(self.name)
         
    def __repr__(self):
        return str(self)

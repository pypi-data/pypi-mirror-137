import torch as tr
from abc import ABC, abstractmethod
from typing import Union, Tuple, Any, Dict
from pathlib import Path
from numbers import Number
from ..types import EpochResultsType

class Callback(ABC):
    """Callback class for NWModules."""
    def __init__(self, name: str):
        assert name is not None
        self.name = name

    # This is used by complex MetricAsCallbacks where we do some stateful computation at every iteration and we want
    #  to reduce it gracefully at the end of the epoch, so it can be stored in trainHistory, as well as for other
    #  callbacks to work nicely with it (SaveModels, PlotCallbacks, etc.). So, we apply a reduction function (default
    #  is identity, which might or might not work depending on algorithm).
    def epoch_reduce_function(self, y: Any) -> Number:
        return y

    def iteration_reduce_function(self, y: Any) -> Number:
        return y

    @abstractmethod
    def on_epoch_start(self, model, working_directory: Path):
        pass

    @abstractmethod
    def on_epoch_end(self, model, epoch_results: EpochResultsType, working_directory: Path) -> Any:
        pass

    @abstractmethod
    def on_iteration_start(self, **kwargs):
        pass

    @abstractmethod
    def on_iteration_end(self, y: tr.Tensor, gt: tr.Tensor, **kwargs) -> Any:
        pass

    # TODO: Replace by save_state_dict/load_state_dict stuff.
    # Some callbacks requires some special/additional tinkering when loading a neural network model from a pickle
    #  binary file (i.e scheduler callbacks must update the optimizer using the new model, rather than the old one).
    #  @param[in] additional Usually is the same as returned by onCallbackSave (default: None)
    def onCallbackLoad(self, additional, **kwargs):
        pass

    # Some callbacks require some special/additional tinkering when saving (such as closing files). It should be noted
    #  that it's safe to close files (or any other side-effect action) because callbacks are deepcopied before this
    #  method is called (in saveModel)
    def onCallbackSave(self, **kwargs):
        pass

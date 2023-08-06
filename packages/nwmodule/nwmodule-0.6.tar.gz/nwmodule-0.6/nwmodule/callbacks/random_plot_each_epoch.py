from typing import Callable, Dict, Any
import torch as tr
from pathlib import Path
from overrides import overrides
from .callback import Callback
from ..types import EpochResultsType

_plotFns = {}
_plotIterationFns = {}

class RandomPlotEachEpoch(Callback):
    # @param[in] Plot function that receives the 3 arguments (x, y, t) for that particular iteration
    # @param[in] baeseDir The subdirectory where the samples are created. By default it's '$(pwd)/samples/'
    # @param[in] plotIterationFn Callback to get the iteration at which the main callback is called.
    #  By default it's 0 (start of epoch).
    def __init__(self, plotFn: Callable, baseDir: str="samples", plotIterationFn=lambda: 0):
        super().__init__(name=f"RandomPlotEachEpoch (Dir='{baseDir}')")
        self.baseDir = baseDir
        self.plotFn = plotFn
        self.plotIterationFn = plotIterationFn
        self.currentEpoch = None
        self.plotIteration = None
        self.working_directory = None

        global _plotFns, _plotIterationFns
        _plotFns[self] = self.plotFn
        _plotIterationFns[self] = self.plotIterationFn

    @overrides
    def on_epoch_start(self, model, working_directory: Path):
        self.currentEpoch = len(model.getTrainHistory()) + 1
        self.plotIteration = self.plotIterationFn()
        self.working_directory = working_directory

    @overrides
    def on_iteration_end(self, y: tr.Tensor, gt: tr.Tensor, **kwargs) -> Any:
        if kwargs["iteration"] != self.plotIteration:
            return
        if kwargs["prefix"] == "Test":
            Dir = self.working_directory / self.baseDir / "test"
        else:
            Dir = f"{self.working_directory}/{self.baseDir}/{self.currentEpoch}/{kwargs['prefix']}"
        Path(Dir).mkdir(exist_ok=True, parents=True)
        self.plotFn(x=kwargs["data"], y=y, t=gt, workingDirectory=Dir)

    def onCallbackLoad(self, additional, **kwargs):
        global _plotFns, _plotIterationFns
        if not self in _plotFns:
            X = tuple(filter(lambda x : isinstance(x, type(self)), kwargs["model"].getCallbacks()))
            assert len(X) == 1
            _plotFns[self] = X[0].plotFn
            _plotIterationFns[self] = X[0].plotIterationFn
        self.plotFn = _plotFns[self]
        self.plotIterationFn = _plotIterationFns[self]

    def onCallbackSave(self, **kwargs):
        self.plotFn = None
        self.plotIterationFn = None

    @overrides
    def on_epoch_end(self, model, epoch_results: EpochResultsType, working_directory: Path) -> Any:
        pass

    @overrides
    def on_iteration_start(self, **kwargs):
        pass

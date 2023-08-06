from typing import Any
from overrides import overrides
from pathlib import Path
import torch as tr

from ..types import EpochResultsType
from .callback import Callback
from ..logger import logger

class SaveHistory(Callback):
    def __init__(self, file_name: str, **kwargs):
        self.file_name = file_name
        super().__init__(name=str(self), **kwargs)

    @overrides
    def on_epoch_start(self, model, working_directory: Path):
        pass

    @overrides
    def on_epoch_end(self, model, epoch_results: EpochResultsType, working_directory: Path) -> Any:
        if not "Train" in epoch_results:
            logger.debug("SaveHistory called in inference mode, not training. Returning early.")
            return

        filePath = working_directory / self.file_name
        file = open(filePath, "w")
        Str = model.summary()
        Str += "\n\n[Train history]"
        epoch = len(model.getTrainHistory())
        for i in range(epoch):
            Str += f"\nEpoch {i + 1}:"
            X = model.getTrainHistory()[i]
            for k in X:
                Str += f"\n- {k}: {X[k]}"
        file.write(Str)
        file.close()

    @overrides
    def onCallbackSave(self, **kwargs):
        pass

    @overrides
    def onCallbackLoad(self, additional, **kwargs):
        pass

    @overrides
    def on_iteration_start(self, **kwargs):
        pass

    @overrides
    def on_iteration_end(self, y: tr.Tensor, gt: tr.Tensor, **kwargs) -> Any:
        pass

    @overrides
    def __str__(self):
        return f"SaveHistory (file: {self.file_name})"

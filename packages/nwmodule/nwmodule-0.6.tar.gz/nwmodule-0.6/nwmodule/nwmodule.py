from abc import abstractmethod, ABC
from typing import List, Union, Dict, Callable, Optional, Iterable, Any
import torch as tr
import torch.nn as nn
import torch.optim as optim
import numpy as np
from collections.abc import Iterable
from types import LambdaType
from nwutils.data_structures import deepCheckEqual
from nwutils.torch import getNumParams, npGetData, trGetData, trToDevice, getOptimizerStr

from .serializer import NWModuleSerializer
from .logger import logger
from .callbacks import Callback
from .metrics import Metric, MetricWrapper, Loss

np.set_printoptions(precision=3, suppress=True)

# Wrapper on top of the PyTorch model. Added methods for saving and loading a state. To completly implement a PyTorch
#  model, one must define layers in the object's constructor, call setOptimizer, setCriterion and implement the
#  forward method identically like a normal PyTorch model.
class NWModule(nn.Module, ABC):
    def __init__(self, hyperParameters:Optional[Dict]=None):
        super().__init__()
        self.optimizer:Optional[optim.Optim] = None
        self.optimizerScheduler = None
        self.serializer = NWModuleSerializer(self)
        self.callbacks = {}
        self.reset_parameters()
        self.hyperParameters = {}
        self.setHyperParameters(hyperParameters)

    @abstractmethod
    def train_step(self, x: Any, **kwargs) -> Any:
        pass

    @abstractmethod
    def inference_step(self, x: Any, **kwargs) -> Any:
        pass

    @abstractmethod
    def criterion(self, y: Any, gt: Any) -> tr.Tensor:
        pass

    @abstractmethod
    def get_trainer_type(self) -> type:
        pass

    ##### Hyperparameters #####

    # @brief Adds hyperparameters to the dictionary. Only works if the model has not been trained yet (so we don't)
    #  update the hyperparameters post-training as it would invalidate the whole principle.
    def setHyperParameters(self, hyperParameters:Dict):
        assert self.hyperParameters == {}, "Clear the existing hyperparameters before setting them. " \
            f"- Current: \n{self.hyperParameters}.\n -New: \n{hyperParameters}"
        hyperParameters = hyperParameters if not hyperParameters is None else {}
        assert isinstance(hyperParameters, dict)
        self.hyperParameters = hyperParameters

    ##### Metrics #####

    def addMetric(self, metric_name: str, metric: Union[Callable, LambdaType, Callback, Metric], direction: str=None):
        # partial or lambda but not metric
        assert isinstance(metric, (Callable, LambdaType, Callback, Metric)), f"Got {type(metric)} for '{metric_name}'"
        if isinstance(metric, (Callable, LambdaType, Callback)) and (not isinstance(metric, Metric)): #type: ignore
            assert direction is not None, "Direction must be set when offering a simple callback as metric."
            metric = MetricWrapper(metric_name, metric, direction) #type: ignore
        if metric_name in self.callbacks:
            raise Exception(f"Metric '{metric_name}' already exists")

        assert metric_name == metric.name
        logger.debug2(f"Adding metric '{metric_name}' ({metric.direction}) to {self}")
        self.callbacks[metric_name] = metric

    # Sets the user provided list of metrics as callbacks and adds them to the callbacks list.
    def addMetrics(self, metrics: List[Metric]):
        assert isinstance(metrics, list), "Metrics must be provided as a list of instantiated metrics"

        for metric in metrics:
            assert isinstance(metric, Metric), "When using addMetrics, all metrics must be already instanciated, " \
                f"got type: {type(metric)} for metric '{metric}'"
            assert metric.name not in self.callbacks, f"Metric {metric.name} already in callbacks list."
            self.addMetric(metric.name, metric)

    def get_default_metrics(self) -> List[Metric]:
        """Gets the default metrics for this module. By default, only loss function, which is generic for all
        modules. This must be overriden to add new default metrics to more specific modules.
        """
        return [Loss()]

    def clearMetrics(self):
        """Clears all the metrics. Only the callbacks are left."""
        callbacks = self.getCallbacks()
        self.callbacks = {k.name: k for k in callbacks}

    def getMetrics(self) -> List[Metric]:
        """Gets all the metrics, no callbacks."""
        return list(filter(lambda x: isinstance(x, Metric), self.callbacks.values()))

    def getMetric(self, metricName) -> Metric:
        """Gets metric by name."""
        for _, callback in self.callbacks.items():
            if not isinstance(callback, Metric):
                continue
            if callback.name == metricName:
                return callback
        assert False, f"Metric {metricName} was not found. Use adddMetrics() properly first."

    def metricsSummary(self) -> str:
        metrics = self.getMetrics()
        summaryStr = ""
        for metric in metrics:
            summaryStr += f"\n  - {metric.name} ({metric.direction})"
        return summaryStr

    ##### Callbacks #####

    def addCallback(self, callback: Callback):
        """Adds a callback to the list of callbacks of this module."""
        logger.debug2(f"Adding callback '{callback.name}' to {self} (type: {type(callback)})")
        assert isinstance(callback, Callback), f"Expected only subclass of types Callback, got type {type(callback)}"
        assert callback.name not in self.callbacks, f"Callback {callback.name} already in callbacks list."
        self.callbacks[callback.name] = callback

    # Adds the user provided list of callbacks to the model's list of callbacks (and metrics)
    def addCallbacks(self, callbacks: List[Callback]):
        """Adds a list of callbacks to this module"""
        for callback in callbacks:
            self.addCallback(callback)

    def clearCallbacks(self):
        """Clears all the callbacks. Only the metrics are left."""
        metrics = self.getMetrics()
        self.callbacks = {k.name: k for k in metrics}

    # Returns only the callbacks that are of subclass Callback (not metrics)
    def getCallbacks(self) -> List[Callback]:
        """Gets all the callbacks."""
        return list(filter(lambda x: not isinstance(x, Metric), self.callbacks.values()))

    def callbacksSummary(self) -> str:
        callbacksStr = ""
        for callback in self.getCallbacks():
            callbacksStr += f"\n  - {callback.name}"
        return callbacksStr


    ##### Training / testing functions #####


    def train_reader_num_steps(self, reader: Iterable, num_steps: int, num_epochs: int,
                               validation_reader: Optional[Iterable]=None, validation_num_steps:int=None, **kwargs):
        return self.get_trainer(**kwargs).train(reader, num_epochs, validation_reader, num_steps, validation_num_steps)

    # @param[in] reader Reader which is used to get items for num_epochs epochs, each taking len(reader) steps
    # @param[in] num_epochs The number of epochs the network is trained for
    # @param[in] validation_reader Validation Reader used to validate the results. If not provided, reader
    #  parameter is used as validation as well for various callbacks (i.e. SaveModels)
    def train_reader(self, reader: Iterable, num_epochs: int, validation_reader: Optional[Iterable]=None, **kwargs):
        validation_num_steps = None if validation_reader is None else len(validation_reader)
        return self.train_reader_num_steps(reader, len(reader), num_epochs, validation_reader,
                                           validation_num_steps, **kwargs)

    # @brief Tests the model given a reader
    # @param[in] reader The input iterator
    # @param[in] num_steps Optional params for the number of steps
    # @return The metrics as given by NWTrainer.test
    def test_reader(self, reader: Iterable, num_steps: Optional[int]=None, **kwargs):
        return self.get_trainer(**kwargs).test(reader, num_steps)

    def hyperParametersSummary(self) -> str:
        hypersStr = ""
        for hyperParameter in self.hyperParameters:
            hypersStr += f"\n  - {hyperParameter}: {self.hyperParameters[hyperParameter]}"
        return hypersStr

    def getNumParams(self):
        return getNumParams(self)

    def summary(self) -> str:
        def format_params(x: int) -> str:
            """1234567890 => 1_234_567_890"""
            try:
                x = int(x)
            except:
                return x
            if x < 1000:
                return x

            x = str(x)
            y = []
            for i in range(len(x)-3, -1, -3):
                y.insert(0, x[i:i+3])
            if i != 0:
                y.insert(0, x[0:i])
            return "_".join(y)

        summaryStr = "[Model summary]"
        summaryStr += f"\n{str(self)}"

        numParams, numTrainable = self.getNumParams()
        numParams, numTrainable = format_params(numParams), format_params(numTrainable)
        summaryStr += f"\nParameters count: {numParams}. Trainable parameters: {numTrainable}."
        summaryStr += f"\nHyperparameters: {self.hyperParametersSummary()}"
        summaryStr += f"\nMetrics: {self.metricsSummary()}"
        summaryStr += f"\nCallbacks: {self.callbacksSummary()}"
        summaryStr += f"\nOptimizer: {self.getOptimizerStr()}"
        summaryStr += f"\nOptimizer Scheduler: {self.optimizerScheduler}"
        summaryStr += f"\nDevice: {self.getDevice()}"

        return summaryStr

    ##### Misc functions #####

    def get_trainer(self, **kwargs):
        return self.get_trainer_type()(self, **kwargs)

    # Wrapper for passing numpy arrays, converting them to torch arrays, forward network and convert back to numpy
    # @param[in] x The input, which can be a numpy array, or a list/tuple/dict of numpy arrays
    # @return y The output of the network as numpy array
    def npForward(self, *args, **kwargs):
        device = self.getDevice()
        tr_args = trToDevice(trGetData(args), device)
        tr_kwargs = trToDevice(trGetData(kwargs), device)
        with tr.no_grad():
            tr_result = self.forward(*tr_args, **tr_kwargs)
        np_result = npGetData(tr_result)
        return np_result

    # @brief Gets the device of the first parameter. Useful to align data with model on the same device (i.e GANs).
    #  Warning! Some models may have parameters on multiple devices (i.e. graphs with edges on multiple GPUs at a time)
    # @return The torch device the first paramter is on.
    def getDevice(self) -> tr.device:
        device = next(self.parameters()).device
        return device

    ##### Load / Save #####
    def saveWeights(self, path):
        return self.serializer.saveModel(path, stateKeys=["weights", "model_state"])

    def loadWeights(self, path, yolo=False):
        logger.debug(f"Loading weights from '{path}'")
        if yolo:
            loadedState = NWModuleSerializer.readPkl(path)
            assert "weights" in loadedState
            logger.debug("YOLO mode. No state & named params check.")
            self.serializer.doLoadWeights(loadedState["weights"], allowNamedMismatch=True)
        else:
            self.serializer.loadModel(path, stateKeys=["model_state", "weights"])

    def saveModel(self, path):
        return self.serializer.saveModel(path, stateKeys=["weights", "optimizer", \
            "history_dict", "callbacks", "model_state"])

    def loadModel(self, path):
        self.serializer.loadModel(path, stateKeys=["weights", "optimizer", "history_dict", "callbacks", "model_state"])

    def onModelSave(self):
        return self.hyperParameters

    def onModelLoad(self, state):
        # if len(self.hyperParameters.keys()) != len(state.keys()):
        # 	return False

        allKeys = set(list(self.hyperParameters.keys()) + list(state.keys()))
        for key in allKeys:
            if not key in self.hyperParameters:
                return False

            if not key in state:
                logger.debug("Warning. Model has unknown state key: %s=%s, possibly added after training. Skipping." \
                    % (key, str(self.hyperParameters[key])))
                continue
            loadedState = state[key]
            modelState = self.hyperParameters[key]

            if not deepCheckEqual(loadedState, modelState):
                return False
        return True


    ##### Other #####

    def isTrainable(self):
        for param in self.parameters():
            if param.requires_grad == True:
                return True
        return False

    def reset_parameters(self):
        # Setup print message keys, callbacks
        self.clearCallbacks()
        self.clearMetrics()
        self.addMetrics(self.get_default_metrics())

        # A list that stores various information about the model at each epoch. The index in the list represents the
        #  epoch value. Each value of the list is a dictionary that holds by default only loss value, but callbacks
        #  can add more items to this (like confusion matrix or accuracy, see mnist example).
        self.trainHistory = []

        children = [x for x in self.children()]
        for layer in children:
            if isinstance(layer, Iterable):
                for i in range(len(layer)):
                    if not hasattr(layer[i], "reset_parameters"):
                        logger.debug(f"Sublayer '{layer[i]}' (type: {type(layer)}) has no reset_parameters() method")
                        continue
                    layer[i].reset_parameters()
            else:
                if not hasattr(layer, "reset_parameters"):
                    logger.debug(f"Sublayer '{layer}' (type: {type(layer)}) has no reset_parameters() method")
                    continue
                layer.reset_parameters()

    ### Getters and setters

    def getTrainHistory(self):
        return self.trainHistory

    def setTrainableWeights(self, value):
        for _, param in self.named_parameters():
            param.requires_grad = value

    # Optimizer can be either a class or an object. If it's a class, it will be instantiated on all the trainable
    #  parameters, and using the arguments in the variable kwargs. If it's an object, we will just use that object,
    #  and assume it's correct (for example if we want only some parameters to be trained this has to be used)
    # Examples of usage: model.setOptimizer(nn.Adam, lr=0.01), model.setOptimizer(nn.Adam(model.parameters(), lr=0.01))
    def setOptimizer(self, optimizer, **kwargs):
        if isinstance(optimizer, optim.Optimizer):
            self.optimizer = optimizer
        else:
            trainableParams = list(filter(lambda p : p.requires_grad, self.parameters()))
            assert len(trainableParams) > 0, "Optimizer must have some trainable parameters."
            self.optimizer = optimizer(trainableParams, **kwargs)
        self.optimizer.storedArgs = kwargs

    def getOptimizer(self):
        return self.optimizer

    def getOptimizerStr(self):
        optimizer = self.getOptimizer()
        return getOptimizerStr(optimizer)

    def setOptimizerScheduler(self, scheduler, **kwargs):
        assert not self.getOptimizer() is None, "Optimizer must be set before scheduler!"
        if isinstance(scheduler, optim.lr_scheduler._LRScheduler):
            self.optimizerScheduler = scheduler
        else:
            self.optimizerScheduler = scheduler(model=self, **kwargs)
            # Some schedulers need acces to the model's object. Others, will not have this argument.
            self.optimizerScheduler.model = self
            self.optimizerScheduler.storedArgs = kwargs

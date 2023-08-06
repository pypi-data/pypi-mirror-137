from overrides import overrides
from nwutils.torch import trToNpCall
from typing import Callable
from .metric import Metric
from ..types import MetricType

class MetricWrapper(Metric):
	def __init__(self, name: str, wrappedMetric: MetricType, direction: str, numpy_fn: bool=False):
		assert isinstance(wrappedMetric, Callable)
		self.wrappedMetric = wrappedMetric
		self.numpy_fn = numpy_fn
		super().__init__(name, direction)

	# @brief The main method that must be implemented by a metric
	@overrides
	def __call__(self, y, gt, **kwargs):
		if self.numpy_fn:
			res = trToNpCall(self.wrappedMetric, y, gt)
		else:
			res = self.wrappedMetric(y, gt)
		return res

	def __str__(self):
		return f"Metric Wrapper ({self.name})"

	def __repr__(self):
		return str(self)

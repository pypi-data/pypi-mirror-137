import torch as tr
from nwmodule import CriterionType
from nwmodule.metrics import MetricWrapper
from torchmetrics import Metric
from typing import List
from overrides import overrides
from functools import partial

from .map_node import MapNode

class Depth(MapNode):
	def __init__(self, maxDepthMeters:float, name:str="depth"):
		self.maxDepthMeters = maxDepthMeters
		hyperParameters = {"maxDepthMeters":maxDepthMeters}
		self.name = name
		MapNode.__init__(self, name, Depth.numDims(), hyperParameters)

	@staticmethod
	def numDims() -> int:
		return 1

	@overrides
	def getNodeMetrics(self) -> List[Metric]:
		metrics = [
			MetricWrapper("RMSE", partial(Depth.rmseMetric, maxDepthMeters=self.maxDepthMeters), "min"),
			MetricWrapper("Depth (m)", partial(Depth.depthMetric, maxDepthMeters=self.maxDepthMeters), "min")
		]
		return metrics

	@overrides
	def getNodeCriterion(self) -> CriterionType:
		return lambda y, gt: Depth.lossFn(y, gt)

	@staticmethod
	def lossFn(y: tr.Tensor, gt: tr.Tensor):
		assert y.shape == gt.shape
		L = ((y - gt)**2).mean()
		return L

	def depthMetric(y: tr.Tensor, gt: tr.Tensor, maxDepthMeters: float, **k) -> float:
		# Normalize back to meters, output is in [0 : 1] representing [0 : maxDepthMeters]m
		yDepthMeters = y * maxDepthMeters
		tDepthMeters = gt * maxDepthMeters
		l1 = tr.abs(yDepthMeters - tDepthMeters).mean()
		return l1

	def rmseMetric(y: tr.Tensor, gt: tr.Tensor, maxDepthMeters: float, **k) -> float:
		# Normalize back to milimeters, output is in [0 : 1] representing [0 : maxDepthMeters]m
		yDepthMeters = y * maxDepthMeters
		tDepthMeters = gt * maxDepthMeters
		L2 = (yDepthMeters - tDepthMeters) ** 2
		rmse = tr.sqrt(L2.mean())
		return rmse

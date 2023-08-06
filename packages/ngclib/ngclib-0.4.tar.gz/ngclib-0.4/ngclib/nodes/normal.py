from typing import List
import numpy as np
import torch as tr
import torch.nn.functional as F
from nwmodule.types import CriterionType
from nwmodule.metrics import MetricWrapper
from torchmetrics import Metric
from overrides import overrides

from .map_node import MapNode

class Normal(MapNode):
	def __init__(self, name: str = "normal"):
		super().__init__(name = name, numDims = 3)

	@overrides
	def getNodeMetrics(self) -> List[Metric]:
		return [
			MetricWrapper("Normal (deg)", Normal.degreeMetric)
		]

	@overrides
	def getNodeCriterion(self) -> CriterionType:
		return Normal.lossFn

	@staticmethod
	def degreeMetric(y: tr.Tensor, gt: tr.Tensor, **k):
		# First, remove sign from both and then do the L1 diff
		y = tr.abs(y)
		gt = tr.abs(gt)
		cosine_distance = F.cosine_similarity(y, gt, dim=-1)
		cosine_distance = cosine_distance.cpu().numpy()
		cosine_distance = np.abs(cosine_distance)
		angles = np.arccos(cosine_distance) / np.pi * 180
		angles[np.isnan(angles)] = 180
		return angles.mean()

	@staticmethod
	def lossFn(y: tr.Tensor, gt: tr.Tensor) -> float:
		return ((y - gt)**2).mean()

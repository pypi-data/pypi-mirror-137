import torch as tr
from typing import List
from overrides import overrides
from torchmetrics.functional import accuracy
from torchmetrics import Metric
from nwmodule import CriterionType
from nwmodule.metrics import MetricWrapper
from nwmodule.loss import sigmoid_bce

from .rgb import RGB
from .map_node import MapNode

class Wireframe(RGB):
	def __init__(self, name:str="wireframe", useGlobalMetrics:bool=False):
		MapNode.__init__(self, name=name, numDims=1)
		self.useGlobalMetrics = useGlobalMetrics
	
	@overrides
	def getNodeMetrics(self) -> List[Metric]:
		metrics = [
			MetricWrapper("Accuracy", lambda y, t : accuracy(y.argmax(-1), t.argmax(-1)), "max")
		]
		# if self.useGlobalMetrics:
		# 	# TODO: These return 0s?
		# 	# metrics["Mean IoU (global)"] = MeanIoU(mode="global")
		# 	# metrics["F1 Score (global)"] = F1Score(mode="global", returnMean=False)
		# 	metrics["Accuracy (global)"] = Accuracy(mode="global")
		return metrics

	@overrides
	def getNodeCriterion(self) -> CriterionType:
		return Wireframe.lossFn

	def lossFn(y: tr.Tensor, t: tr.Tensor) -> float:
		return sigmoid_bce(y[..., 0], t[..., 0]).mean()

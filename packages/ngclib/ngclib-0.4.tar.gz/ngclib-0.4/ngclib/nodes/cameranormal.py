from copy import deepcopy
from typing import List
from torchmetrics import Metric
from overrides import overrides

from .map_node import MapNode
from .normal import Normal

class CameraNormal(Normal):
	def __init__(self, name: str="cameranormal"):
		MapNode.__init__(self, name=name, numDims=3)

	@overrides
	def getNodeMetrics(self) -> List[Metric]:
		metrics = super().getNodeMetrics()
		new_metrics = []
		for metric in metrics:
			new_metric = deepcopy(metric)
			new_metric.name = metric.name.replace("Normal", "CameraNormal")
			new_metrics.append(new_metric)
		return new_metrics

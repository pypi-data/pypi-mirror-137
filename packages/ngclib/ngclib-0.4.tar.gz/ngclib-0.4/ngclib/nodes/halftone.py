from copy import deepcopy
from typing import List
from overrides import overrides
from torchmetrics import Metric

from .map_node import MapNode
from .rgb import RGB

class Halftone(RGB):
	def __init__(self, name:str="halftone"):
		MapNode.__init__(self, name=name, numDims=3)

	@overrides
	def getNodeMetrics(self) -> List[Metric]:
		metrics = super().getNodeMetrics()
		new_metrics = []
		for metric in metrics:
			new_metric = deepcopy(metric)
			new_metric.name = metric.name.replace("RGB", "Halftone")
			new_metrics.append(new_metric)
		return new_metrics

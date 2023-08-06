from copy import deepcopy
from typing import List
from overrides import overrides
from torchmetrics import Metric

from .rgb import RGB
from .map_node import MapNode

class SoftSegmentation(RGB):
	def __init__(self, name: str="softsegmentation"):
		MapNode.__init__(self, name=name, numDims=3)

	@overrides
	def getNodeMetrics(self) -> List[Metric]:
		metrics = super().getNodeMetrics()
		new_metrics = []
		for metric in metrics:
			new_metric = deepcopy(metric)
			new_metric.name = metric.name.replace("RGB", "SoftSegmentation")
			new_metrics.append(new_metric)
		return new_metrics

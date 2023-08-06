from typing import List, Dict
from overrides import overrides
from nwgraph import Node
from nwmodule.models import FeedForwardNetwork
from .ngc_edge import NGCEdge

class SingleLink(NGCEdge, FeedForwardNetwork):
    """Simple Single Link edge. Defined by a regular forward pass."""
    def __init__(self, inputNode: Node, outputNode: Node, hyperParameters: Dict = {}):
        name = f"Single Link ({inputNode} -> {outputNode})"
        prefix = "SL"
        super().__init__(prefix, inputNode, outputNode, name, hyperParameters)

    @overrides
    def getInKeys(self) -> List[str]:
        return [self.inputNode.name]

    def inference_step(self):
        # assert len(self.inputNode.messages) == 1
        # message = tuple(self.inputNode.messages)[0]
        return [self.forward(message.input) for message in self.inputNode.messages]

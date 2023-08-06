from copy import deepcopy
from typing import Dict, List
from numpy import concatenate
import torch as tr
from overrides import overrides
from torch import nn
from nwmodule import NWModule
from nwutils.nwmodule import trModuleWrapper
from nwutils.torch import trGetData
from nwgraph import Node
from ..edges import NGCEdge
from ...logger import logger

class SingleLinkResidual(NGCEdge):
    def __init__(self, residualNode: Node, inputNode: Node, outputNode: Node, hyperParameters: Dict={}):
        hyperParameters["residualNode"] = residualNode
        name = f"Single Link Residual ({inputNode} -> {outputNode}) (Residual Node: {residualNode})"
        prefix = "SLR"
        super().__init__(prefix, inputNode, outputNode, name, hyperParameters)
        self.residualNode = residualNode

    @overrides
    def getModel(self) -> NWModule:
        if hasattr(self, "model"):
            logger.info("Model already instantiated, returning early.")
            return self.model
        A, B = self.inputNode, self.outputNode
        # Create a new intermediate node where we append the SL's (RGB) numbers of dimensions to instantaite the model
        #  properly.
        _A = deepcopy(A)
        _A.numDims += self.hyperParameters["residualNode"].numDims
        encoder = _A.getEncoder(B)
        decoder = B.getDecoder(A)
        model = trModuleWrapper(nn.Sequential(encoder, decoder))
        return model

    def train_step(self, x, **kwargs):
        residual = x[self.residualNode]
        edge_input = x[self.inputNode]
        concatenated = tr.cat([edge_input, residual], dim=-1)
        return self.forward(concatenated)

    def inference_step(self):
        assert len(self.residualNode.messages) == 1
        residual = tuple(self.residualNode.messages)[0].input
        res = []
        n_inputs = len(self.inputNode.messages)
        for i in range(n_inputs):
            edge_input = tuple(self.inputNode.messages)[i].input
            concatenated = tr.cat([edge_input, residual], dim=-1)
            res.append(self.forward(concatenated))
        return res

    @overrides
    def getInKeys(self) -> List[str]:
        return [self.inputNode.name, self.residualNode.name]

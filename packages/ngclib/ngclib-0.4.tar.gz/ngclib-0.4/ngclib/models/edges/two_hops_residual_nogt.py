from copy import copy
from typing import Dict, List
import torch as tr
from pathlib import Path
from overrides import overrides
from torch import nn
from nwmodule import NWModule
from nwutils.nwmodule import trModuleWrapper
from nwutils.torch import trGetData
from nwgraph import Edge, Node
from .two_hops_nogt import TwoHopsSerializer
from .ngc_edge import NGCEdge
from ...logger import logger

class TwoHopsResidualNoGT(NGCEdge):
    def __init__(self, singleLinkEdge: Edge, residualNode: Node, \
            inputNode: Node, outputNode: Node, hyperParameters: Dict={}):
        singleLinkNode = singleLinkEdge.inputNode
        name = f"Two Hops Residual NoGT ({inputNode} -> {outputNode}) (Single Link Node: {singleLinkNode}. " \
            f"Residual Node: {residualNode})"
        prefix = "THR_NOGT"
        hyperParameters["singleLinkNode"] = singleLinkNode
        hyperParameters["residualNode"] = residualNode
        super().__init__(prefix, inputNode, outputNode, name, hyperParameters)

        self.singleLinkNode = singleLinkNode
        self.residualNode = residualNode
        self.singleLinkEdge = singleLinkEdge
        self.serializer = TwoHopsSerializer(model=self)
        logger.debug(f"Setting single link of {self.name}: '{self.singleLinkEdge}'")

    @overrides
    def getModel(self) -> NWModule:
        if hasattr(self, "model"):
            logger.info("Model already instantiated, returning early.")
            return self.model
        A, B = self.inputNode, self.outputNode
        # Create a new intermediate node where we append the SL's (RGB) numbers of dimensions to instantaite the model
        #  properly.
        _A = copy(A)
        _A.numDims += self.hyperParameters["residualNode"].numDims
        encoder = _A.getEncoder(B)
        decoder = B.getDecoder(A)
        model = trModuleWrapper(nn.Sequential(encoder, decoder))
        return model

    @overrides
    def setup(self, **kwargs):
        weightsFile = f"{kwargs['singleLinkDir']}/model_best_Loss.pkl" 
        logger.debug(f"Loading single link of {self.name}: {self.singleLinkEdge} from '{weightsFile}'")
        self.singleLinkEdge = copy(self.singleLinkEdge).to(self.getDevice())
        self.singleLinkEdge.setTrainableWeights(True)
        self.singleLinkEdge.loadWeights(weightsFile)
        self.singleLinkEdge.eval()

    def train_step(self, x, **kwargs):
        with tr.no_grad():
            sl_output = self.singleLinkEdge.train_step(x)
        residual = x[self.residualNode]
        concatenated = tr.cat([sl_output, residual], dim=-1)
        return self.forward(concatenated)

    def inference_step(self):
        assert len(self.residualNode.messages) == 1
        residual = tuple(self.residualNode.messages)[0].input
        sl_outputs = self.singleLinkEdge.inference_step()
        res = []
        for sl_output in sl_outputs:    
            concatenated = tr.cat([sl_output, residual], dim=-1)
            res.append(self.forward(concatenated))
        return res

    @overrides
    def getInKeys(self) -> List[str]:
        return self.singleLinkEdge.getInKeys()


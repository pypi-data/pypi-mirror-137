import torch as tr
from overrides import overrides
from typing import Any, Dict, List
from copy import copy
from nwgraph import Node, Edge
from nwmodule.serializer import NWModuleSerializer
from .ngc_edge import NGCEdge
from ...logger import logger

device = tr.device("cuda") if tr.cuda.is_available() else tr.device("cpu")

class TwoHopsSerializer(NWModuleSerializer):
    @overrides
    def doSaveWeights(self):
        # Guarantee that the single link is not trainable at save time, so it's not saved.
        isTrainable = self.model.singleLinkEdge.isTrainable()
        self.model.singleLinkEdge.setTrainableWeights(False)
        parametersState = super().doSaveWeights()
        self.model.singleLinkEdge.setTrainableWeights(isTrainable)
        return parametersState

    @overrides
    def doLoadWeights(self, loadedParams, allowNamedMismatch=False):
        # Temporarily remove the reference to the single link edge from the two hops model so we can load w/o these
        #  names missing from the state_dict.
        slEdge = self.model.singleLinkEdge
        self.model.singleLinkEdge = None
        super().doLoadWeights(loadedParams, allowNamedMismatch)
        self.model.singleLinkEdge = slEdge

class TwoHopsNoGT(NGCEdge):
    def __init__(self, singleLinkEdge: Edge, inputNode: Node, outputNode: Node, hyperParameters: Dict={}):
        singleLinkNode = singleLinkEdge.inputNode
        name = f"Two Hops NoGT ({inputNode} -> {outputNode}) (Single Link Node: {singleLinkNode})"
        prefix = "TH_NOGT"
        hyperParameters["singleLinkNode"] = singleLinkNode
        super().__init__(prefix, inputNode, outputNode, name, hyperParameters)
        self.singleLinkNode = singleLinkNode
        self.singleLinkEdge = singleLinkEdge
        self.serializer = TwoHopsSerializer(model=self)
        logger.debug(f"Setting single link of {self.name}: '{self.singleLinkEdge}'")

    @overrides
    def setup(self, **kwargs):
        weightsFile = f"{kwargs['singleLinkDir']}/model_best_Loss.pkl" 
        logger.debug(f"Loading single link of {self.name}: {self.singleLinkEdge} from '{weightsFile}'")
        # TODO: THIS is because sometimes when training in parallel, and multiple TH edegs have the same SL, it gets
        #  messed up with the device.
        self.singleLinkEdge = copy(self.singleLinkEdge).to(self.getDevice())
        self.singleLinkEdge.setTrainableWeights(True)
        self.singleLinkEdge.loadWeights(weightsFile)
        self.singleLinkEdge.eval()

    @overrides
    def train_step(self, x: Any, **kwargs) -> Any:
        with tr.no_grad():
            sl_output = self.singleLinkEdge.train_step(x)
        return self.forward(sl_output, **kwargs)

    def inference_step(self) -> Any:
        sl_outputs = self.singleLinkEdge.inference_step()
        return [self.forward(sl_output) for sl_output in sl_outputs]

    @overrides
    def getInKeys(self) -> List[str]:
        return self.singleLinkEdge.getInKeys()

from pathlib import Path
from typing import Dict
from overrides import overrides
from .edge_trainer import EdgeTrainer, get_loader
from .setup_edge import setup_edge
from ..readers import NGCNpzReader
from ..logger import logger

class EdgeTrainerSequential(EdgeTrainer):
    @overrides
    def run(self, trainCfg: Dict, trainReader: NGCNpzReader, validationReader: NGCNpzReader, debug: bool):
        if debug:
            trainCfg["numEpochs"] = 3
        weightsDir = Path.cwd()

        trained = self.model.getTrainedEdges(weightsDir, EdgeTrainer.getEdgeDirName)
        for edge in self.model.edges:
            setup_edge(edge, trainCfg, weightsDir)
            if edge in trained:
                logger.debug(f"Edge '{edge}' already trained. Skipping.")
                continue

            trainLoader = get_loader(trainReader, edge, trainCfg, randomize=True, debug=debug, augmentation=True)
            valLoader = get_loader(validationReader, edge, trainCfg, randomize=False, debug=debug, augmentation=False)

            Dir = Path.cwd() / EdgeTrainer.getEdgeDirName(edge)
            edge.get_trainer(workingDirectory=Dir).train(trainLoader, trainCfg["numEpochs"], valLoader)
            del valLoader, trainLoader

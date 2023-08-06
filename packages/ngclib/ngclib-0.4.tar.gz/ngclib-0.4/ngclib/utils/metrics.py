import numpy as np
import torch as tr
import torch.nn.functional as F
from typing import Dict, Callable
from copy import deepcopy
from collections import OrderedDict
from sklearn.metrics import f1_score, jaccard_score
from scipy.special import softmax
from torchmetrics.functional import accuracy
from nwgraph import Node
from nwutils.torch import npToTrCall

from ..nodes import Semantic

def get_metrics_semantic(y: np.ndarray, gt: np.ndarray, node: Semantic) -> Dict:
    if y.shape[-1] == node.numClasses:
        one_hot_y = y
        softmax_y = softmax(one_hot_y, axis=-1)
        argmax_y = np.argmax(one_hot_y, -1)
    else:
        argmax_y = y
        one_hot_y = F.one_hot(tr.from_numpy(argmax_y).type(tr.int64), node.numClasses).type(tr.float32)
        softmax_y = one_hot_y

    if gt.shape[-1] == node.numClasses:
        argmax_t = np.argmax(gt, -1).astype(np.uint8)
    else:
        argmax_t = gt.astype(np.uint8)
    one_hot_t = F.one_hot(tr.from_numpy(argmax_t).type(tr.int64), node.numClasses).type(tr.float32)

    argmax_y = argmax_y.flatten()
    argmax_t = argmax_t.flatten()

    metrics = OrderedDict({
        "Loss": float(npToTrCall(node.getNodeCriterion(), one_hot_y, one_hot_t)),
        "Accuracy": lambda y, t: float(npToTrCall(accuracy, argmax_y, argmax_t)),
        "Mean IoU": lambda y, t : jaccard_score(argmax_y, argmax_t, average=None, labels=range(node.numClasses)),
        "F1 Score": lambda y, t : f1_score(argmax_y, argmax_t, average=None, labels=range(node.numClasses)),
    })
    return metrics

# For a given node with a set of predictions and GT, return all the node's metrics.
# Some hardcoded stuff for Semantic, until we figure out if we can generalize it better.
def getMetrics(y: np.ndarray, gt: np.ndarray, node: Node) -> Dict:
    if isinstance(node, Semantic):
        metrics = get_metrics_semantic(y, gt, node)
    else:
        metrics = OrderedDict(node.getNodeMetrics())
        metrics["Loss"] = npToTrCall(node.getNodeCriterion(), y, gt)
    # res = {k:metrics[k](y, gt) for k in metrics.keys()}
    res = deepcopy(metrics)

    for k in metrics:
        if isinstance(metrics[k], Callable):
            metrics[k] = metrics[k](y, gt)
        res[k] = metrics[k]
        if isinstance(metrics[k], np.ndarray):
            res[k] = list(res[k])
            res[f"{k} (mean)"] = metrics[k].mean()
    return res

from typing import Any, List
from overrides import overrides
import torch as tr
import torch.nn as nn
from nwutils.nwmodule import trModuleWrapper
from nwmodule import NWModule
from nwmodule.metrics import Metric

from .edge import Edge
from ..logger import logger

class SimpleEdge(Edge):
    @overrides
    def getModel(self) -> NWModule:
        if hasattr(self, "model"):
            logger.info("Model already instantiated, returning early.")
            return self.model
        A, B = self.inputNode, self.outputNode
        encoder = A.getEncoder(B)
        decoder = B.getDecoder(A)
        model = trModuleWrapper(nn.Sequential(encoder, decoder))
        return model

    @overrides
    def criterion(self, y: Any, gt: Any) -> tr.Tensor:
        return self.outputNode.getNodeCriterion()(y, gt)

    @overrides
    def get_default_metrics(self) -> List[Metric]:
        """Add all nodes metrics to the edge."""
        metrics = super().get_default_metrics()
        for metric in self.outputNode.getNodeMetrics():
            if metric in metrics:
                continue
            metrics.append(metric)
        return metrics

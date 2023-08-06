from abc import abstractmethod
from typing import Any, Dict, List, Set, Iterable, Optional
from overrides import overrides
import torch as tr
import torch.nn as nn
from nwmodule import NWModule

from .draw_graph import drawGraph
from .graph_serializer import GraphSerializer
from .graph_trainer import GraphTrainer
from .message import Message
from .node import Node
from .edge import Edge
from .logger import logger

# A Graph is a list of Edges. Each edge is a FeedForward network between two nodes.
class Graph(NWModule):
    def __init__(self, edges, hyperParameters={}):
        self.nodes = self.getNodesFromEdges(edges)
        self.edges = edges
        hyperParameters = self.getHyperParameters(hyperParameters, self.nodes, edges)
        super().__init__(hyperParameters=hyperParameters)
        self.edges = nn.ModuleList(self.edges)

        # (A, B) => Edge(A, B)
        self.edgeLosses = {k : [] for k in self.edges}
        self.serializer = GraphSerializer(model=self)
        self.nameToNodes = {node.name:node for node in self.nodes}

    @abstractmethod
    # @brief Method that defines how messages are sent in one iteration.
    def messagePass(self, t: int):
        pass
    
    @abstractmethod
    # @brief Aggregate function must transform all the received messages of a node to one message after all iterations
    #  have been finished. Basically f(node, [message]) = (node, message).
    def aggregate(self):
        pass

    @abstractmethod
    def backprop_node_losses(self, y: Any, gt: Any) -> Dict[str, List[float]]:
        """Defines how the backpropagation step is done w.r.t the nodes, resulting a list of losses,
        one for each message"""
        pass

    # TODO?
    # @abstractmethod
    # def backprop_edge_losses(self, gt: Any) -> Dict[str, List[float]]:
    #     """Defines how the backpropagation step is done, resulting a dict of edges, containing a list of losses, one
    #     for each message."""
    #     pass
    
    @abstractmethod
    def backprop_graph_loss(self, edge_losses: Dict[str, List[float]]) -> float:
        """Defines how the backpropagation step is done using the result from self.backprop_edge_losses(gt) """

    @overrides
    def train_step(self, x: Any, **kwargs) -> Any:
        return self.forward(x, **kwargs)

    @overrides
    def inference_step(self, x: Any, **kwargs) -> Any:
        return self.forward(x, **kwargs)

    @overrides
    def criterion(self, y: Any, gt: Any) -> tr.Tensor:
        node_losses = self.backprop_node_losses(y, gt)
        graph_loss = self.backprop_graph_loss(node_losses)
        return graph_loss

    @overrides
    def get_trainer_type(self) -> type:
        return GraphTrainer

    # @brief The forward pass/message passing of a graph. The algorithm is as follows:
    #  - x represents the "external" data of this passing
    #  - each forward call will send all possible messages of each node to all possible neightbours
    #  - x[node] is the new data (if it exists) for this node. Otherwise, only messages from the previous pass are used
    #  - After all the iterations are done, a reduce call is issued, which, for each node reduces the messages to a
    #  potential less number of messages.
    def forward(self, x, numIterations: int = 1):
        self._clear_messages()
        self._add_gt_to_nodes(x)
        for i in range(numIterations):
            self.messagePass(i)
        self.aggregate()
        y = self._get_node_messages()
        return y

    def _add_gt_to_nodes(self, data):
        # Add potential GT messages, if any.
        for node in self.nodes:
            if not node.name in data:
                continue
            # Both input and output are the same tensor, with the "GT" path. 
            message = Message([f"GT ({node.name})"], data[node.name], data[node.name])
            node.addMessage(message)

    def _clear_messages(self):
        logger.debug2("Clearing node messages.")
        for node in self.nodes:
            node.clearMessages()

    def _get_node_messages(self) -> List[Message]:
        return {k : k.getMessages() for k in self.nodes}

    def getEdges(self) -> List[Edge]:
        edges = []
        for edge in self.edges:
            edges.append(edge)
        return edges

    def getNodeByName(self, name: str) -> Node:
        return self.nameToNodes[name]

    def getNodesFromEdges(self, edges: List[Edge]) -> Set[Node]:
        if hasattr(self, "nodes"):
            return self.nodes

        nodes = set()
        nameToNodes = {}
        for edge in edges:
            A, B = edge.getNodes()
            nodes.add(A)
            nodes.add(B)
            if A.name in nameToNodes:
                assert nameToNodes[A.name] == A
            if B.name in nameToNodes:
                assert nameToNodes[B.name] == B
            nameToNodes[A.name] = A
            nameToNodes[B.name] = B
        return nodes

    def draw(self, fileName, cleanup=True, view=False):
        drawGraph(self.nodes, self.edges, fileName, cleanup, view)

    # We also override some methods on the Network class so it works with edges as well.

    @overrides
    def setOptimizer(self, optimizer, **kwargs):
        logger.debug(f"Settings the optimizer '{optimizer}' for all edges. This might overwrite optimizers!")
        # assert isinstance(optimizer, type), "TODO For more special cases: %s" % type(optimizer)
        for edge in self.edges:
            if edge.getNumParams()[1] == 0:
                logger.debug(f"Skipping edge '{edge}' as it has no trainable parameters!")
                continue
            edge.setOptimizer(optimizer, **kwargs)

    @overrides
    def getOptimizerStr(self):
        strList = super().getOptimizerStr()
        for edge in self.edges:
            strEdge = str(edge)
            if type(edge) == Graph:
                strEdge = "SubGraph"
            edgeStrList = edge.getOptimizerStr()
            strList.extend(edgeStrList)
        return strList

    def getHyperParameters(self, hyperParameters:Dict, nodes:List[Node], edges:List[Edge]) -> Dict:
        # Set up hyperparameters for every node
        hyperParameters = {k : hyperParameters[k] for k in hyperParameters}
        for node in nodes:
            hyperParameters[node.name] = node.hyperParameters
        for edge in edges:
            hyperParameters[str(edge)] = edge.hyperParameters
        return hyperParameters

    def graphStr(self, depth=1):
        Str = "Graph:"
        pre = "  " * depth
        for edge in self.edges:
            if type(edge) == Graph:
                edgeStr = edge.graphStr(depth + 1)
            else:
                edgeStr = str(edge)
            Str += f"\n{pre}-{edgeStr}"
        return Str

    def __str__(self) -> str:
        return self.graphStr()

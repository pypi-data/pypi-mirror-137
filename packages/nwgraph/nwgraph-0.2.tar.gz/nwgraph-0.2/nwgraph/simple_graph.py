from typing import Dict, Any, List
from overrides import overrides
from .message import Message
from .graph import Graph
from .logger import logger
from .graph_trainer import mean

class SimpleGraph(Graph):
    @overrides
    # @brief Send all messages to all possible neighbours.
    def messagePass(self, t: int):
        for edge in self.edges:
            A, B = edge.getNodes()
            for message in A.getMessages():
                y = edge.forward(message.output)
                newMessagePath = [*message.path, edge]
                newMessage = Message(newMessagePath, message.output, y)
                B.addMessage(newMessage)

    @overrides
    # @brief Simplest aggregation step. Do nothing.
    def aggregate(self):
        pass

    @overrides
    def backprop_node_losses(self, y: Any, gt: Any) -> Dict[str, List[float]]:
        """Gets the loss of all edges by passing through all the nodes, and the via all the messages."""
        # breakpoint()
        logger.debug2(f"Computing nodes losses from all nodes that produced messages ({len(y)} nodes).")
        node_losses = {}
        for node in y.keys():
            f_criterion = node.getNodeCriterion()
            if f_criterion is None:
                logger.debug2(f"Skipping node {node}, because no criterion is available")
                continue
            if not node.name in gt:
                logger.debug2(f"Skipping node {node}, because no gt is available")
                continue

            node_outputs = [x.output for x in node.messages]
            node_losses[node] = [f_criterion(x, gt[node.name]) for x in node_outputs]
        logger.debug2(f"Passed through all nodes.")
        return node_losses

    @overrides
    def backprop_graph_loss(self, edge_losses: Dict[str, List[float]]) -> float:
        L = []
        for edge in edge_losses.keys():
            edge_loss = edge_losses[edge]
            if len(edge_loss) == 0:
                continue
            edge_loss = mean(edge_loss)
            L.append(edge_loss)
        L = mean(L)
        return L

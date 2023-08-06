from pathlib import Path
from overrides import overrides
from nwmodule import NWModule
from nwmodule.trainer import NWTrainer
from .edge import Edge
from .logger import logger

def mean(x, default=0) : return sum(x) / len(x) if len(x) > 0 else default

class GraphTrainer(NWTrainer):
    def __init__(self, model: NWModule, working_directory: Path=None, num_iterations_per_forward: int=1):
        super().__init__(model, working_directory)
        self.num_iterations_per_forward = num_iterations_per_forward

    @staticmethod
    @overrides
    def do_optimizer_step(model: NWModule, loss: float):
        for edge in model.edges:
            if edge.getOptimizer() is None:
                continue
            edge.getOptimizer().zero_grad()
        loss.backward(retain_graph=False)
        for edge in model.edges:
            if edge.getOptimizer() is None:
                continue
            edge.getOptimizer().step()

    @overrides
    def train_step(self, x, gt, is_optimizing: bool):
        logger.debug2(f"Passing through all the edges for {self.num_iterations_per_forward} iteration.")
        node_messages = self.model.forward(x, numIterations=self.num_iterations_per_forward)

        logger.debug2("Computing graph loss.")
        graph_loss = self.model.criterion(node_messages, gt)
        logger.debug2("Computed graph loss.")

        if is_optimizing:
            GraphTrainer.do_optimizer_step(self.model, graph_loss)
        return node_messages, graph_loss

    @overrides
    def callbacksOnIterationEnd(self, x, gt, y, loss, iteration, numIterations, metricResults, prefix):
        # Nodes accumulate messages only if part of a graph. A normal edge is just a simple feed forward network with
        #  no special semantics, like message passing.
        def edgeLevelIterationEnd(edge, labels, edgeLosses):
            metrics = edge.getMetrics()
            edgeResult = {k.name: [] for k in metrics}
            messages = edge.getNodes()[1].getMessages()
            for message in messages:
                assert len(message.path) > 0
                lastPath = message.path[-1]
                if not isinstance(lastPath, Edge) or lastPath != edge:
                    continue
                for metric in metrics:
                    y = message.output
                    t = labels
                    loss = mean(edgeLosses[edge], default=0)
                    res = metric(y, t, loss=loss)
                    edgeResult[metric.name].append(res)

            # Do the mean of all messages, if any result exists.
            for metric in metrics:
                edgeResult[metric.name] = mean(edgeResult[metric], default=[])
            return edgeResult

        def nodeLevelIterationEnd(node, labels):
            metrics = node.getNodeMetrics()
            nodeResult = {k.name: [] for k in metrics}
            messages = node.getMessages()
            for message in messages:
                for metric in metrics:
                    y = message.output
                    t = labels
                    res = metric(y, t)
                    nodeResult[metric.name].append(res)

            # Do the mean of all messages, if any result exists.
            for metric in metrics:
                nodeResult[metric.name] = mean(nodeResult[metric], default=[])
            return nodeResult

        # Graph level metrics
        graphResults = super().callbacksOnIterationEnd(x, gt, y, loss, iteration, numIterations, metricResults, prefix)

        # Edge level metrics
        edgeResults = {}
        for edge in self.model.edges:
            outputNode = edge.outputNode
            if not outputNode.name in gt:
                continue
            edgeLabels = gt[outputNode.name]
            edgeResults[edge.name] = edgeLevelIterationEnd(edge, edgeLabels, self.model.edgeLosses)
        graphResults["edges"] = edgeResults

        # Node level metrics
        nodeResults = {}
        for node in self.model.nodes:
            if not node.name in gt:
                continue
            nodeLabels = gt[node.name]
            nodeResults[node.name] = nodeLevelIterationEnd(node, nodeLabels)
        metricResults["nodes"] = nodeResults

        return metricResults

    @overrides
    def epochPrologue(self, epochResults):
        res = super().epochPrologue(epochResults)
        
        nodeResults, edgeResults = {}, {}
        for edge in self.model.edges:
            X = {}
            for K in epochResults:
                if not edge in epochResults[K]["edges"]:
                    continue
                X[K] = epochResults[K]["edges"][edge]
                for metricName in X[K]:
                    X[K][metricName] = edge.getMetric(metricName).epoch_reduce_function(X[K][metricName])
            if len(X) > 0:
                edgeResults[str(edge)] = X
        
        for node in self.model.nodes:
            X = {}
            for K in epochResults:
                if not node in epochResults[K]["nodes"]:
                    continue
                X[K] = epochResults[K]["nodes"][node]
            if len(X) > 0:
                nodeResults[str(node)] = X
        
        res["edges"] = edgeResults
        res["nodes"] = nodeResults
        return res

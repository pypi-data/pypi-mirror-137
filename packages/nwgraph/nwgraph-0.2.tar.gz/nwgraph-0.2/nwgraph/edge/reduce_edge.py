from typing import Callable
from nwutils.nwmodule import trModuleWrapper
from .edge import Edge
from ..node import Node

class ReduceEdge(Edge):
	"""A loop edge for the same node. Used to aggregate a single node."""
	def __init__(self, inputNode: Node, forwardFn: Callable, *args, **kwargs):
		self.forwardFn = forwardFn
		self.inputNode = inputNode
		super().__init__(inputNode, inputNode, *args, **kwargs)

	def forward(self, x):
		return self.forwardFn(x, self)

	def getDecoder(self):
		return trModuleWrapper(lambda x: x)

	def getEncoder(self):
		return trModuleWrapper(lambda x: x)

	def criterion(self, y, gt):
		return self.inputNode.getNodeCriterion()(y, gt)

	def getModel(self):
		pass

	def __str__(self):
		return f"ReduceEdge {self.inputNode}"

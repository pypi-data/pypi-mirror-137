# file stubs/ogdf/CircleGraph.py generated from classogdf_1_1_circle_graph
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class CircleGraph(ogdf.Graph):

	def __init__(self, C : ClusterStructure, toCircle : NodeArray[node], c : int) -> None:
		...

	def fromCircle(self, vCircle : node) -> node:
		...

	def order(self, nodeList : List[node]) -> None:
		...

	def swapping(self, nodeList : List[node], maxIterations : int) -> None:
		...

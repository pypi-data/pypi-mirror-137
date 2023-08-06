# file stubs/ogdf/fast_multipole_embedder/NodeMassComparer.py generated from classogdf_1_1fast__multipole__embedder_1_1_node_mass_comparer
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class NodeMassComparer(object):

	def __init__(self, nodeState : NodeArray[GalaxyMultilevelBuilder.LevelNodeState]) -> None:
		...

	def __call__(self, a : GalaxyMultilevelBuilder.NodeOrderInfo, b : GalaxyMultilevelBuilder.NodeOrderInfo) -> bool:
		...

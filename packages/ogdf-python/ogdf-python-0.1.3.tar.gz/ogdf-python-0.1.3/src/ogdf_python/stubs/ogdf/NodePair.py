# file stubs/ogdf/NodePair.py generated from structogdf_1_1_node_pair
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class NodePair(object):

	source : node = ...

	target : node = ...

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, src : node, tgt : node) -> None:
		...

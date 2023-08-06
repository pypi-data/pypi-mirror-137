# file stubs/ogdf/dot/Ast/NodeId.py generated from structogdf_1_1dot_1_1_ast_1_1_node_id
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class NodeId(ogdf.dot.Ast.EdgeLhs):

	id : str = ...

	port : Port = ...

	def __init__(self, idString : str, paramPort : Port) -> None:
		...

	def __destruct__(self) -> None:
		...

	def read(self, P : Parser, G : ogdf.Graph, GA : GraphAttributes, C : ClusterGraph, CA : ClusterGraphAttributes, data : SubgraphData) -> bool:
		...

# file stubs/ogdf/BertaultLayout/__init__.py generated from classogdf_1_1_bertault_layout
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class BertaultLayout(ogdf.LayoutModule):

	@overload
	def __init__(self) -> None:
		"""Constructor, sets options to default values."""
		...

	@overload
	def __init__(self, length : float, number : int) -> None:
		"""Constructor, with user defined values for required length and number of iterations."""
		...

	@overload
	def __init__(self, number : int) -> None:
		"""Constructor, with user defined values for number of iterations."""
		...

	def __destruct__(self) -> None:
		...

	def call(self, AG : GraphAttributes) -> None:
		"""The main call to the algorithm. AG should have nodeGraphics and EdgeGraphics attributes enabled."""
		...

	def edgeCrossings(self, AG : GraphAttributes) -> int:
		"""Calculates the edge crossings in the graph corresponding to AG. Node attributes required."""
		...

	def edgelength(self, GA : GraphAttributes) -> float:
		"""Calculates the normalised standard deviation of edge lengths in the graph corresponding to AG. Node attributes required."""
		...

	def initPositions(self, AG : GraphAttributes, c : int) -> None:
		"""Set the initPositions of nodes."""
		...

	@overload
	def iterno(self) -> int:
		"""Returns the number of iterations."""
		...

	@overload
	def iterno(self, no : int) -> None:
		"""Sets the number of iterations. Ifno<= 0, 10*n will be used."""
		...

	def nodeDistribution(self, GA : GraphAttributes) -> float:
		"""Gives a measure of the node distribution in the graph corresponding to AG. The lesser the value, the more uniform the distribution. Node attributes required."""
		...

	@overload
	def reqlength(self) -> float:
		"""Returns the required length."""
		...

	@overload
	def reqlength(self, length : float) -> None:
		"""Sets the required length. Iflength<= 0, the average edge length will be used."""
		...

	def setImpred(self, option : bool) -> None:
		"""Sets impred option true or false."""
		...

	def compute_I(self, v : node, e : edge, AG : GraphAttributes) -> None:
		"""Computes the projection of node v on the edge (a,b)"""
		...

	def f_Edge(self, v : node, e : edge, AG : GraphAttributes) -> None:
		"""Calculates the repulsive force on node v due to the edge on which node i lies and adds it to total force on v."""
		...

	def f_Node_Attractive(self, v : node, j : node, AG : GraphAttributes) -> None:
		"""Calculates the attractive force on node v due to node j and adds it to total force on v."""
		...

	def f_Node_Repulsive(self, v : node, j : node, AG : GraphAttributes) -> None:
		"""Calculates the repulsive force on node v due to node j and adds it to total force on v."""
		...

	def i_On_Edge(self, e : edge, AG : GraphAttributes) -> bool:
		"""Returns true if node i lies on the edge (a,b)"""
		...

	def move(self, v : node, AG : GraphAttributes) -> None:
		"""Moves the node v according to the forces Fx and Fy on it. Also ensures that movement is within the respective zones."""
		...

	def r_Calc_On_Edge(self, v : node, e : edge, AG : GraphAttributes) -> None:
		"""Calculates the radii of the zones of node v if node i lies on edge (a,b)"""
		...

	def r_Calc_Outside_Edge(self, v : node, e : edge, AG : GraphAttributes) -> None:
		"""Calculates the radii of the zones of node v if node i does not lie on edge (a,b)"""
		...

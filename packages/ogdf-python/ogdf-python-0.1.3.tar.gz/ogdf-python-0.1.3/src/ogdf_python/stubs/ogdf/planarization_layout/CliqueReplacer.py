# file stubs/ogdf/planarization_layout/CliqueReplacer.py generated from classogdf_1_1planarization__layout_1_1_clique_replacer
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class CliqueReplacer(object):

	def __init__(self, ga : GraphAttributes, G : Graph) -> None:
		...

	def centerNodes(self) -> SListPure[node]:
		...

	def cliquePos(self, v : node) -> DPoint:
		...

	def cliqueRect(self, v : node) -> DRect:
		...

	@overload
	def computeCliquePosition(self, adjNodes : List[node], center : node, rectMin : float = -1.0) -> None:
		...

	@overload
	def computeCliquePosition(self, center : node, rectMin : float) -> None:
		...

	def getDefaultCliqueCenterSize(self) -> float:
		...

	def isReplacement(self, e : edge) -> bool:
		"""returns true if edge was inserted during clique replacement"""
		...

	def replaceByStar(self, cliques : List[List[node]  ]) -> None:
		...

	def setDefaultCliqueCenterSize(self, i : float) -> None:
		...

	def undoStar(self, center : node, restoreAllEdges : bool) -> None:
		...

	def undoStars(self) -> None:
		...

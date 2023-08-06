# file stubs/ogdf/MinSTCutModule.py generated from classogdf_1_1_min_s_t_cut_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
TCost = TypeVar('TCost')

class MinSTCutModule(Generic[TCost]):

	m_direction : EdgeArray[  int ] = ...

	m_gc : GraphCopy = ...

	def __init__(self) -> None:
		"""default constructor (empty)"""
		...

	def __destruct__(self) -> None:
		...

	@overload
	def call(self, graph : Graph, weight : EdgeArray[ TCost ], s : node, t : node, edgeList : List[edge], e_st : edge = None) -> bool:
		"""The actual algorithm call."""
		...

	@overload
	def call(self, graph : Graph, s : node, t : node, edgeList : List[edge], e_st : edge = None) -> bool:
		"""The actual algorithm call."""
		...

	def direction(self, e : edge) -> bool:
		"""Returns the direction ofein the cut."""
		...

	def preprocessingDual(self, graph : Graph, gc : GraphCopy, CE : CombinatorialEmbedding, source : node, target : node, e_st : edge) -> bool:
		"""This method preprocessesgcfor minstcut calculations, by adding an st-edge if needed and embeddinggc."""
		...

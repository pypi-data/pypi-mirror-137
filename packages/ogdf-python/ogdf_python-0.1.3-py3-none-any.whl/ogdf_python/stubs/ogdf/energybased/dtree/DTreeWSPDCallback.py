# file stubs/ogdf/energybased/dtree/DTreeWSPDCallback.py generated from classogdf_1_1energybased_1_1dtree_1_1_d_tree_w_s_p_d_callback
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
Dim = TypeVar('Dim')

UseForcePrime = TypeVar('UseForcePrime')

ForceFunc = TypeVar('ForceFunc')

class DTreeWSPDCallback(Generic[Dim, ForceFunc, UseForcePrime]):

	m_forceFunc : ForceFunc = ...

	m_treeForce : DTreeForce[ Dim ] = ...

	def __init__(self, treeForce : DTreeForce[ Dim ], forceFunc : ForceFunc) -> None:
		...

	def onWellSeparatedPair(self, a : int, b : int) -> None:
		"""called by the WSPD for well separated pair"""
		...

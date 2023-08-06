# file stubs/ogdf/IncNodeInserter.py generated from classogdf_1_1_inc_node_inserter
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class IncNodeInserter(object):

	#: pointer to aPlanRepIncthat is to be changed
	m_planRep : PlanRepInc = ...

	def __init__(self, PG : PlanRepInc) -> None:
		"""Creates inserter onPG."""
		...

	def insertCopyNode(self, v : node, E : CombinatorialEmbedding, vTyp : Graph.NodeType) -> None:
		"""Inserts copy inm_planRepfor original nodev."""
		...

	def getInsertionFace(self, v : node, E : CombinatorialEmbedding) -> face:
		"""Returns a face to insert a copy ofvand a list of adjacency entries corresponding to the insertion adjEntries for the adjacent edges."""
		...

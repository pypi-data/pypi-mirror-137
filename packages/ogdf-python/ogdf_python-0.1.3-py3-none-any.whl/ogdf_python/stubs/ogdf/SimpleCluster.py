# file stubs/ogdf/SimpleCluster.py generated from classogdf_1_1_simple_cluster
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class SimpleCluster(object):

	m_size : int = ...

	def __init__(self, parent : SimpleCluster = None) -> None:
		...

	def children(self) -> SList[SimpleCluster]:
		...

	def getIndex(self) -> int:
		...

	def getParent(self) -> SimpleCluster:
		...

	def nodes(self) -> SList[node]:
		...

	def pushBackChild(self, s : SimpleCluster) -> None:
		...

	def pushBackVertex(self, v : node) -> None:
		...

	def setIndex(self, index : int) -> None:
		...

	def setParent(self, parent : SimpleCluster) -> None:
		...

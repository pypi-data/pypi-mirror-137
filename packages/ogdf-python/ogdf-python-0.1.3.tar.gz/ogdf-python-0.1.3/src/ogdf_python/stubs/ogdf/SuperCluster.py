# file stubs/ogdf/SuperCluster.py generated from structogdf_1_1_super_cluster
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class SuperCluster(object):

	m_cluster : SList[  int ] = ...

	m_direction : float = ...

	m_length : float = ...

	m_scaleFactor : float = ...

	def __init__(self, clusters : SList[  int ], direction : float, length : float, scaleFactor : float = 1.0) -> None:
		...

# file stubs/ogdf/ClusterRegion.py generated from structogdf_1_1_cluster_region
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ClusterRegion(object):

	m_clusters : SList[  int ] = ...

	m_length : float = ...

	m_scaleFactor : float = ...

	m_start : float = ...

	def __init__(self, c : int, start : float, length : float, scaleFactor : float = 1.0) -> None:
		...

# file stubs/ogdf/SCRegion.py generated from structogdf_1_1_s_c_region
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class SCRegion(object):

	m_length : float = ...

	m_start : float = ...

	m_superClusters : SList[SuperCluster] = ...

	def __init__(self, sc : SuperCluster) -> None:
		...

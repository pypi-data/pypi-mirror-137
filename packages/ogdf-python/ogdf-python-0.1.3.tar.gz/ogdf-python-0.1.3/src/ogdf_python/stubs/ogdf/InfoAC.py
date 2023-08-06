# file stubs/ogdf/InfoAC.py generated from structogdf_1_1_info_a_c
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class InfoAC(object):

	m_parentCluster : int = ...

	m_predCut : node = ...

	m_predCutBC : node = ...

	m_vBC : node = ...

	def __init__(self, vBC : node, predCutBC : node, predCut : node, parentCluster : int) -> None:
		...

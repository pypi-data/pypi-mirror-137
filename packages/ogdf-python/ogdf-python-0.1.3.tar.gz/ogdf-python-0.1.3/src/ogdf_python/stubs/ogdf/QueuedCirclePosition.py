# file stubs/ogdf/QueuedCirclePosition.py generated from structogdf_1_1_queued_circle_position
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class QueuedCirclePosition(object):

	m_cluster : int = ...

	m_minDist : float = ...

	m_sectorEnd : float = ...

	m_sectorStart : float = ...

	def __init__(self, clusterIdx : int, minDist : float, sectorStart : float, sectorEnd : float) -> None:
		...

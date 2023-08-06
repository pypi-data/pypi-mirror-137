# file stubs/ogdf/QueueEntry.py generated from structogdf_1_1_queue_entry
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class QueueEntry(object):

	m_current : node = ...

	m_parent : node = ...

	def __init__(self, p : node, v : node) -> None:
		...

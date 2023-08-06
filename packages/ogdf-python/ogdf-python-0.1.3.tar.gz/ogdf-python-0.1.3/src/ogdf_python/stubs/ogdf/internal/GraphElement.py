# file stubs/ogdf/internal/GraphElement.py generated from classogdf_1_1internal_1_1_graph_element
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class GraphElement(object):

	"""The base class for objects used by (hyper)graphs."""

	#: The successor in the list.
	m_next : GraphElement = ...

	#: The predecessor in the list.
	m_prev : GraphElement = ...

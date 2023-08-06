# file stubs/ogdf/cluster_planarity/edgeValue.py generated from structogdf_1_1cluster__planarity_1_1edge_value
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class edgeValue(object):

	"""Struct for attaching the current lp-value to the corresponding edge. Used in the primal heuristic."""

	e : edge = ...

	lpValue : float = ...

	original : bool = ...

	src : node = ...

	trg : node = ...

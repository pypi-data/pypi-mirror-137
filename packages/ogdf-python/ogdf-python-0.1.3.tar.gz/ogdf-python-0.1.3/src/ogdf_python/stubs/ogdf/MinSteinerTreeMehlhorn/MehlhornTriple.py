# file stubs/ogdf/MinSteinerTreeMehlhorn/MehlhornTriple.py generated from structogdf_1_1_min_steiner_tree_mehlhorn_1_1_mehlhorn_triple
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class MehlhornTriple(object):

	"""Represents a triple as specified in the algorithms description (see paper)"""

	bridge : edge = ...

	u : node = ...

	v : node = ...

	value : T = ...

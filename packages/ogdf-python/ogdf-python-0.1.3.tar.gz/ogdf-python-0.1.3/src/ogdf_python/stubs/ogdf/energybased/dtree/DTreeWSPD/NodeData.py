# file stubs/ogdf/energybased/dtree/DTreeWSPD/NodeData.py generated from structogdf_1_1energybased_1_1dtree_1_1_d_tree_w_s_p_d_1_1_node_data
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class NodeData(object):

	"""geometry for the quadtree nodes"""

	#: bounding box min coord
	max_x : float = ...

	#: bounding box min coord
	min_x : float = ...

	#: radius of the cell
	radius_sq : float = ...

	#: center of cell circle
	x : float = ...

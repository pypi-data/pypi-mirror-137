# file stubs/ogdf/fast_multipole_embedder/GalaxyMultilevel/LevelNodeInfo.py generated from structogdf_1_1fast__multipole__embedder_1_1_galaxy_multilevel_1_1_level_node_info
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class LevelNodeInfo(object):

	mass : float = ...

	nearSuns : NearSunList = ...

	parent : node = ...

	radius : float = ...

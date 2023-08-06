# file stubs/ogdf/LayerByLayerSweep/CrossMinMaster.py generated from classogdf_1_1_layer_by_layer_sweep_1_1_cross_min_master
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class CrossMinMaster(object):

	def __init__(self, sugi : SugiyamaLayout, H : Hierarchy, runs : int) -> None:
		...

	def doWorkHelper(self, pCrossMin : LayerByLayerSweep, pCrossMinSimDraw : TwoLayerCrossMinSimDraw, levels : HierarchyLevels, bestPos : NodeArray[  int ], permuteFirst : bool, rng : std.minstd_rand) -> None:
		...

	def hierarchy(self) -> Hierarchy:
		...

	def restore(self, levels : HierarchyLevels, cr : int) -> None:
		...

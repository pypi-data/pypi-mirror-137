# file stubs/ogdf/energybased/fmmm/Multilevel.py generated from classogdf_1_1energybased_1_1fmmm_1_1_multilevel
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Multilevel(object):

	def create_multilevel_representations(self, G : Graph, A : NodeArray[NodeAttributes], E : EdgeArray[EdgeAttributes], rand_seed : int, galaxy_choice : FMMMOptions.GalaxyChoice, min_Graph_size : int, rand_tries : int, G_mult_ptr : Array[Graph], A_mult_ptr : Array[NodeArray[NodeAttributes]  ], E_mult_ptr : Array[EdgeArray[EdgeAttributes]  ], max_level : int) -> None:
		"""The multilevel representations *G_mult_ptr/*A_mult_ptr/*E_mult_ptr for G/A/E are created. The maximum multilevel is calculated, too."""
		...

	def delete_multilevel_representations(self, G_mult_ptr : Array[Graph], A_mult_ptr : Array[NodeArray[NodeAttributes]  ], E_mult_ptr : Array[EdgeArray[EdgeAttributes]  ], max_level : int) -> None:
		"""Free dynamically allocated memory."""
		...

	def find_initial_placement_for_level(self, level : int, init_placement_way : FMMMOptions.InitialPlacementMult, G_mult_ptr : Array[Graph], A_mult_ptr : Array[NodeArray[NodeAttributes]  ], E_mult_ptr : Array[EdgeArray[EdgeAttributes]  ]) -> None:
		"""The initial placement of the nodes at multilevel level are created by the placements of the nodes of the graphs at the lower level (if init_placement_way is 0) or additionally using information of the actual level ( if init_placement_way == 1). Precondition: level < max_level."""
		...

# file stubs/ogdf/energybased/fmmm/ParticleListState.py generated from structogdf_1_1energybased_1_1fmmm_1_1_particle_list_state
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ParticleListState(object):

	"""Returned state fortraverse()"""

	#: Last left item.
	lastLeft : ListIterator[ParticleInfo] = ...

	#: Left particle list is empty.
	leftEmpty : bool = ...

	#: Left particle list is larger.
	leftLarger : bool = ...

	#: Right particle list is empty.
	rightEmpty : bool = ...

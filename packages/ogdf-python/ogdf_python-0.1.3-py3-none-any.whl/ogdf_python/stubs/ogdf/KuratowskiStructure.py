# file stubs/ogdf/KuratowskiStructure.py generated from classogdf_1_1_kuratowski_structure
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class KuratowskiStructure(object):

	"""A Kuratowski Structure is a special graph structure containing severals subdivisions."""

	#: The root of the bicomp containingstopXandstopY.
	R : node = ...

	#: Real node of virtual nodeR.
	RReal : node = ...

	#: First stopping node.
	stopX : node = ...

	#: Second stopping node.
	stopY : node = ...

	#: The current node to embed.
	V : node = ...

	#: DFI of the current node to embed.
	V_DFI : int = ...

	#: External face path of bicomp containingVin direction CCW.
	externalFacePath : SListPure[adjEntry] = ...

	#: A list of all edges in all externally active paths (bundles only)
	externalSubgraph : SListPure[edge] = ...

	#: Listof externally active nodes strictly between x and y for minortypesBandE.
	externE : SListPure[ExternE] = ...

	#: The whole highestFacePath of the bicomp containingV.
	highestFacePath : ArrayBuffer[adjEntry] = ...

	#: The appropriate paths of the highestFacePath for each wNode.
	highestXYPaths : SListPure[ArrayBuffer[adjEntry] ] = ...

	#: A list of all edges in pertinent paths (bundles only)
	pertinentSubgraph : SListPure[edge] = ...

	#: Listof all endnodes of paths starting atstopX(only without bundles)
	stopXEndnodes : SListPure[node] = ...

	#: Listof all virtual startnodes of paths starting atstopX(only without bundles)
	stopXStartnodes : SListPure[  int ] = ...

	#: Listof all endnodes of paths starting atstopY(only without bundles)
	stopYEndnodes : SListPure[node] = ...

	#: Listof all virtual startnodes of paths starting atstopY(only without bundles)
	stopYStartnodes : SListPure[  int ] = ...

	#: Holds information about all pertinent nodeswof the bicomp containingV.
	wNodes : SListPure[WInfo] = ...

	#: A path from thezNodein minortypeDto nodeVfor each highest XY-Path.
	zPaths : SListPure[ArrayBuffer[adjEntry] ] = ...

	@overload
	def __init__(self) -> None:
		"""Constructor."""
		...

	@overload
	def __init__(self, orig : KuratowskiStructure) -> None:
		"""Copy constructor."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...

	def clear(self) -> None:
		"""Reset all data members."""
		...

	def __assign__(self, orig : KuratowskiStructure) -> KuratowskiStructure:
		"""Assignment."""
		...

	def copy(self, orig : KuratowskiStructure) -> None:
		"""Copies class."""
		...

	def copyPointer(self, orig : KuratowskiStructure, list : SListPure[WInfo]) -> None:
		"""Used in copy constructor."""
		...

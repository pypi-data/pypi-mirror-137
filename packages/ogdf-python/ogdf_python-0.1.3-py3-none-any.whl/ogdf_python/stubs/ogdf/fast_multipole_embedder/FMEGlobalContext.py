# file stubs/ogdf/fast_multipole_embedder/FMEGlobalContext.py generated from structogdf_1_1fast__multipole__embedder_1_1_f_m_e_global_context
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class FMEGlobalContext(object):

	"""Global Context."""

	coolDown : float = ...

	currAvgEdgeLength : float = ...

	#: var for the main thread to notify the other threads that they are done
	earlyExit : bool = ...

	#: the global node force x array
	globalForceX : float = ...

	#: the global node force y array
	globalForceY : float = ...

	#: global point, node max x coordinate for bounding box calculations
	max_x : float = ...

	#: global point, node max y coordinate for bounding box calculations
	max_y : float = ...

	#: global point, node min x coordinate for bounding box calculations
	min_x : float = ...

	#: global point, node min y coordinate for bounding box calculations
	min_y : float = ...

	#: number of threads, local contexts
	numThreads : int = ...

	#: pointer to the coeefficients
	pExpansion : LinearQuadtreeExpansion = ...

	#: pointer to the array graph
	pGraph : ArrayGraph = ...

	#: all local contexts
	pLocalContext : FMELocalContext = ...

	#: pointer to the global options
	pOptions : FMEGlobalOptions = ...

	#: pointer to the quadtree
	pQuadtree : LinearQuadtree = ...

	#: pointer to the well separated pairs decomposition
	pWSPD : WSPD = ...

	#: var
	scaleFactor : float = ...

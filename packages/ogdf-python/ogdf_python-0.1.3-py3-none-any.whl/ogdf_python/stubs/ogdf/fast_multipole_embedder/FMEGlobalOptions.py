# file stubs/ogdf/fast_multipole_embedder/FMEGlobalOptions.py generated from structogdf_1_1fast__multipole__embedder_1_1_f_m_e_global_options
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class FMEGlobalOptions(object):

	"""the main global options for a run"""

	#: enable postprocessing
	doPostProcessing : bool = ...

	#: enable preprocessing
	doPrepProcessing : bool = ...

	#: edge force factor for the main step
	edgeForceFactor : float = ...

	#: maximum number of iterations in the main step
	maxNumIterations : int = ...

	#: minimum number of iterations to be done regardless of any other conditions
	minNumIterations : int = ...

	multipolePrecision : int = ...

	#: average edge length when desired edge length are normalized
	normEdgeLength : float = ...

	#: average node size when node sizes are normalized
	normNodeSize : float = ...

	#: edge force factor for the preprocessing step
	preProcEdgeForceFactor : float = ...

	#: number of iterations the preprocessing is applied
	preProcMaxNumIterations : int = ...

	#: time step factor for the preprocessing step
	preProcTimeStep : float = ...

	#: repulsive force factor for the main step
	repForceFactor : float = ...

	#: stopping criteria
	stopCritAvgForce : float = ...

	#: stopping criteria
	stopCritConstSq : float = ...

	#: stopping criteria
	stopCritForce : float = ...

	#: time step factor for the main step
	timeStep : float = ...

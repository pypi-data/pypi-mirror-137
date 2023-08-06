# file stubs/ogdf/FMMMOptions.py generated from classogdf_1_1_f_m_m_m_options
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class FMMMOptions(object):

	class AllowedPositions(enum.Enum):

		"""Specifies which positions for a node are allowed."""

		#: Every position is allowed.
		All = enum.auto()

		#: Only integer positions are allowed that are in a range depending on the number of nodes and the average ideal edge length.
		Integer = enum.auto()

		#: Only integer positions in a range of -2^MaxIntPosExponent to 2^MaxIntPosExponent are alllowed.
		Exponent = enum.auto()

	class EdgeLengthMeasurement(enum.Enum):

		"""Specifies how the length of an edge is measured."""

		#: Measure from center point of edge end points.
		Midpoint = enum.auto()

		#: Measure from border of circle s surrounding edge end points.
		BoundingCircle = enum.auto()

	class ForceModel(enum.Enum):

		"""Specifies the force model."""

		#: The force-model by Fruchterman, Reingold.
		FruchtermanReingold = enum.auto()

		#: The force-model by Eades.
		Eades = enum.auto()

		#: The new force-model.
		New = enum.auto()

	class GalaxyChoice(enum.Enum):

		"""Specifies how sun nodes of galaxies are selected."""

		#: selecting by uniform random probability
		UniformProb = enum.auto()

		#: selecting by non-uniform probability depending on the star masses (prefering nodes with lower star mass)
		NonUniformProbLowerMass = enum.auto()

		#: as above but prefering nodes with higher star mass
		NonUniformProbHigherMass = enum.auto()

	class InitialPlacementForces(enum.Enum):

		"""Specifies how the initial placement is done."""

		#: Uniform placement on a grid.
		UniformGrid = enum.auto()

		#: Random placement (based on current time).
		RandomTime = enum.auto()

		#: Random placement (based on randIterNr()).
		RandomRandIterNr = enum.auto()

		#: No change in placement.
		KeepPositions = enum.auto()

	class InitialPlacementMult(enum.Enum):

		"""Specifies how the initial placement is generated."""

		#: only using information about placement of nodes on higher levels
		Simple = enum.auto()

		#: using additional information about the placement of all inter solar system nodes
		Advanced = enum.auto()

	class MaxIterChange(enum.Enum):

		"""Specifies how MaxIterations is changed in subsequent multilevels."""

		#: kept constant at the force calculation step at every level
		Constant = enum.auto()

		#: linearly decreasing from MaxIterFactor*FixedIterations to FixedIterations
		LinearlyDecreasing = enum.auto()

		#: rapdily decreasing from MaxIterFactor*FixedIterations to FixedIterations
		RapidlyDecreasing = enum.auto()

	class PageFormatType(enum.Enum):

		"""Possible page formats."""

		#: A4 portrait page.
		Portrait = enum.auto()

		#: A4 landscape page.
		Landscape = enum.auto()

		#: Square format.
		Square = enum.auto()

	class PreSort(enum.Enum):

		"""Specifies how connected components are sorted before the packing algorithm is applied."""

		#: Do not presort.
		_None = enum.auto()

		#: Presort by decreasing height of components.
		DecreasingHeight = enum.auto()

		#: Presort by decreasing width of components.
		DecreasingWidth = enum.auto()

	class QualityVsSpeed(enum.Enum):

		"""Trade-off between run-time and quality."""

		#: Best quality.
		GorgeousAndEfficient = enum.auto()

		#: Medium quality and speed.
		BeautifulAndFast = enum.auto()

		#: Best speed.
		NiceAndIncredibleSpeed = enum.auto()

	class ReducedTreeConstruction(enum.Enum):

		"""Specifies how the reduced bucket quadtree is constructed."""

		#: Path-by-path construction.
		PathByPath = enum.auto()

		#: Subtree-by-subtree construction.
		SubtreeBySubtree = enum.auto()

	class RepulsiveForcesMethod(enum.Enum):

		"""Specifies how to calculate repulsive forces."""

		#: Exact calculation (slow).
		Exact = enum.auto()

		#: Grid approximation (inaccurate).
		GridApproximation = enum.auto()

		#: Calculation as for new multipole method (fast and accurate).
		NMM = enum.auto()

	class SmallestCellFinding(enum.Enum):

		"""Specifies how to calculate the smallest quadratic cell that surrounds the particles of a node in the reduced bucket quadtree."""

		#: Iteratively (in constant time).
		Iteratively = enum.auto()

		#: According to formula by Aluru et al.
		Aluru = enum.auto()

	class StopCriterion(enum.Enum):

		"""Specifies the stop criterion."""

		#: Stop if fixedIterations() is reached.
		FixedIterations = enum.auto()

		#: Stop if threshold() is reached.
		Threshold = enum.auto()

		#: Stop if fixedIterations() or threshold() is reached.
		FixedIterationsOrThreshold = enum.auto()

	class TipOver(enum.Enum):

		"""Specifies in which case it is allowed to tip over drawings of connected components."""

		#: not allowed at all
		_None = enum.auto()

		#: only if the height of the packing row does not grow
		NoGrowingRow = enum.auto()

		#: always allowed
		Always = enum.auto()

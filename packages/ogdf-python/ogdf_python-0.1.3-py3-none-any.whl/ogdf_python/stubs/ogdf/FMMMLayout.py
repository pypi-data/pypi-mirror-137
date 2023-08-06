# file stubs/ogdf/FMMMLayout.py generated from classogdf_1_1_f_m_m_m_layout
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class FMMMLayout(ogdf.LayoutModule):

	"""The fast multipole multilevel layout algorithm."""

	# The algorithm call

	@overload
	def call(self, GA : GraphAttributes) -> None:
		"""Calls the algorithm for graphGAand returns the layout information inGA."""
		...

	@overload
	def call(self, GA : ClusterGraphAttributes) -> None:
		"""Calls the algorithm for clustered graphGAand returns the layout information inGA. Models cluster by simple edge length adaption based on least common ancestor cluster of end vertices."""
		...

	@overload
	def call(self, GA : GraphAttributes, edgeLength : EdgeArray[ float ]) -> None:
		"""Extended algorithm call: Allows to pass desired lengths of the edges."""
		...

	@overload
	def call(self, GA : GraphAttributes, ps_file : str) -> None:
		"""Extended algorithm call: Calls the algorithm for graphGA."""
		...

	@overload
	def call(self, GA : GraphAttributes, edgeLength : EdgeArray[ float ], ps_file : str) -> None:
		"""Extend algorithm call: Allows to pass desired lengths of the edges."""
		...

	# Further information.

	def getCpuTime(self) -> float:
		"""Returns the runtime (=CPU-time) of the layout algorithm in seconds."""
		...

	# High-level options

	@overload
	def useHighLevelOptions(self) -> bool:
		"""Returns the current setting of option useHighLevelOptions."""
		...

	@overload
	def useHighLevelOptions(self, uho : bool) -> None:
		"""Sets the option useHighLevelOptions touho."""
		...

	def setSingleLevel(self, b : bool) -> None:
		"""Sets single level option, no multilevel hierarchy is created if b == true."""
		...

	@overload
	def pageFormat(self) -> FMMMOptions.PageFormatType:
		"""Returns the current setting of option pageFormat."""
		...

	@overload
	def pageFormat(self, t : FMMMOptions.PageFormatType) -> None:
		"""Sets the option pageRatio tot."""
		...

	@overload
	def unitEdgeLength(self) -> float:
		"""Returns the current setting of option unitEdgeLength."""
		...

	@overload
	def unitEdgeLength(self, x : float) -> None:
		"""Sets the option unitEdgeLength tox."""
		...

	@overload
	def newInitialPlacement(self) -> bool:
		"""Returns the current setting of option newInitialPlacement."""
		...

	@overload
	def newInitialPlacement(self, nip : bool) -> None:
		"""Sets the option newInitialPlacement tonip."""
		...

	@overload
	def qualityVersusSpeed(self) -> FMMMOptions.QualityVsSpeed:
		"""Returns the current setting of option qualityVersusSpeed."""
		...

	@overload
	def qualityVersusSpeed(self, qvs : FMMMOptions.QualityVsSpeed) -> None:
		"""Sets the option qualityVersusSpeed toqvs."""
		...

	# General low-level options

	@overload
	def randSeed(self, p : int) -> None:
		"""Sets the seed of the random number generator."""
		...

	@overload
	def randSeed(self) -> int:
		"""Returns the seed of the random number generator."""
		...

	@overload
	def edgeLengthMeasurement(self) -> FMMMOptions.EdgeLengthMeasurement:
		"""Returns the current setting of option edgeLengthMeasurement."""
		...

	@overload
	def edgeLengthMeasurement(self, elm : FMMMOptions.EdgeLengthMeasurement) -> None:
		"""Sets the option edgeLengthMeasurement toelm."""
		...

	@overload
	def allowedPositions(self) -> FMMMOptions.AllowedPositions:
		"""Returns the current setting of option allowedPositions."""
		...

	@overload
	def allowedPositions(self, ap : FMMMOptions.AllowedPositions) -> None:
		"""Sets the option allowedPositions toap."""
		...

	@overload
	def maxIntPosExponent(self) -> int:
		"""Returns the current setting of option maxIntPosExponent."""
		...

	@overload
	def maxIntPosExponent(self, e : int) -> None:
		"""Sets the option maxIntPosExponent toe."""
		...

	# Options for the divide et impera step

	@overload
	def pageRatio(self) -> float:
		"""Returns the current setting of option pageRatio."""
		...

	@overload
	def pageRatio(self, r : float) -> None:
		"""Sets the option pageRatio tor."""
		...

	@overload
	def stepsForRotatingComponents(self) -> int:
		"""Returns the current setting of option stepsForRotatingComponents."""
		...

	@overload
	def stepsForRotatingComponents(self, n : int) -> None:
		"""Sets the option stepsForRotatingComponents ton."""
		...

	@overload
	def tipOverCCs(self) -> FMMMOptions.TipOver:
		"""Returns the current setting of option tipOverCCs."""
		...

	@overload
	def tipOverCCs(self, to : FMMMOptions.TipOver) -> None:
		"""Sets the option tipOverCCs toto."""
		...

	@overload
	def minDistCC(self) -> float:
		"""Returns the minimal distance between connected components."""
		...

	@overload
	def minDistCC(self, x : float) -> None:
		"""Sets the minimal distance between connected components tox."""
		...

	@overload
	def presortCCs(self) -> FMMMOptions.PreSort:
		"""Returns the current setting of option presortCCs."""
		...

	@overload
	def presortCCs(self, ps : FMMMOptions.PreSort) -> None:
		"""Sets the option presortCCs tops."""
		...

	# Options for the multilevel step

	@overload
	def minGraphSize(self) -> int:
		"""Returns the current setting of option minGraphSize."""
		...

	@overload
	def minGraphSize(self, n : int) -> None:
		"""Sets the option minGraphSize ton."""
		...

	@overload
	def galaxyChoice(self) -> FMMMOptions.GalaxyChoice:
		"""Returns the current setting of option galaxyChoice."""
		...

	@overload
	def galaxyChoice(self, gc : FMMMOptions.GalaxyChoice) -> None:
		"""Sets the option galaxyChoice togc."""
		...

	@overload
	def randomTries(self) -> int:
		"""Returns the current setting of option randomTries."""
		...

	@overload
	def randomTries(self, n : int) -> None:
		"""Sets the option randomTries ton."""
		...

	@overload
	def maxIterChange(self) -> FMMMOptions.MaxIterChange:
		"""Returns the current setting of option maxIterChange."""
		...

	@overload
	def maxIterChange(self, mic : FMMMOptions.MaxIterChange) -> None:
		"""Sets the option maxIterChange tomic."""
		...

	@overload
	def maxIterFactor(self) -> int:
		"""Returns the current setting of option maxIterFactor."""
		...

	@overload
	def maxIterFactor(self, f : int) -> None:
		"""Sets the option maxIterFactor tof."""
		...

	@overload
	def initialPlacementMult(self) -> FMMMOptions.InitialPlacementMult:
		"""Returns the current setting of option initialPlacementMult."""
		...

	@overload
	def initialPlacementMult(self, ipm : FMMMOptions.InitialPlacementMult) -> None:
		"""Sets the option initialPlacementMult toipm."""
		...

	# Options for the force calculation step

	@overload
	def forceModel(self) -> FMMMOptions.ForceModel:
		"""Returns the used force model."""
		...

	@overload
	def forceModel(self, fm : FMMMOptions.ForceModel) -> None:
		"""Sets the used force model tofm."""
		...

	@overload
	def springStrength(self) -> float:
		"""Returns the strength of the springs."""
		...

	@overload
	def springStrength(self, x : float) -> None:
		"""Sets the strength of the springs tox."""
		...

	@overload
	def repForcesStrength(self) -> float:
		"""Returns the strength of the repulsive forces."""
		...

	@overload
	def repForcesStrength(self, x : float) -> None:
		"""Sets the strength of the repulsive forces tox."""
		...

	@overload
	def repulsiveForcesCalculation(self) -> FMMMOptions.RepulsiveForcesMethod:
		"""Returns the current setting of option repulsiveForcesCalculation."""
		...

	@overload
	def repulsiveForcesCalculation(self, rfc : FMMMOptions.RepulsiveForcesMethod) -> None:
		"""Sets the option repulsiveForcesCalculation torfc."""
		...

	@overload
	def stopCriterion(self) -> FMMMOptions.StopCriterion:
		"""Returns the stop criterion."""
		...

	@overload
	def stopCriterion(self, rsc : FMMMOptions.StopCriterion) -> None:
		"""Sets the stop criterion torsc."""
		...

	@overload
	def threshold(self) -> float:
		"""Returns the threshold for the stop criterion."""
		...

	@overload
	def threshold(self, x : float) -> None:
		"""Sets the threshold for the stop criterion tox."""
		...

	@overload
	def fixedIterations(self) -> int:
		"""Returns the fixed number of iterations for the stop criterion."""
		...

	@overload
	def fixedIterations(self, n : int) -> None:
		"""Sets the fixed number of iterations for the stop criterion ton."""
		...

	@overload
	def forceScalingFactor(self) -> float:
		"""Returns the scaling factor for the forces."""
		...

	@overload
	def forceScalingFactor(self, f : float) -> None:
		"""Sets the scaling factor for the forces tof."""
		...

	@overload
	def coolTemperature(self) -> bool:
		"""Returns the current setting of option coolTemperature."""
		...

	@overload
	def coolTemperature(self, b : bool) -> None:
		"""Sets the option coolTemperature tob."""
		...

	@overload
	def coolValue(self) -> float:
		"""Returns the current setting of option coolValue."""
		...

	@overload
	def coolValue(self, x : float) -> None:
		"""Sets the option coolValue tox."""
		...

	@overload
	def initialPlacementForces(self) -> FMMMOptions.InitialPlacementForces:
		"""Returns the current setting of option initialPlacementForces."""
		...

	@overload
	def initialPlacementForces(self, ipf : FMMMOptions.InitialPlacementForces) -> None:
		"""Sets the option initialPlacementForces toipf."""
		...

	# Options for the postprocessing step

	@overload
	def resizeDrawing(self) -> bool:
		"""Returns the current setting of option resizeDrawing."""
		...

	@overload
	def resizeDrawing(self, b : bool) -> None:
		"""Sets the option resizeDrawing tob."""
		...

	@overload
	def resizingScalar(self) -> float:
		"""Returns the current setting of option resizingScalar."""
		...

	@overload
	def resizingScalar(self, s : float) -> None:
		"""Sets the option resizingScalar tos."""
		...

	@overload
	def fineTuningIterations(self) -> int:
		"""Returns the number of iterations for fine tuning."""
		...

	@overload
	def fineTuningIterations(self, n : int) -> None:
		"""Sets the number of iterations for fine tuning ton."""
		...

	@overload
	def fineTuneScalar(self) -> float:
		"""Returns the curent setting of option fineTuneScalar."""
		...

	@overload
	def fineTuneScalar(self, s : float) -> None:
		"""Sets the option fineTuneScalar tos."""
		...

	@overload
	def adjustPostRepStrengthDynamically(self) -> bool:
		"""Returns the current setting of option adjustPostRepStrengthDynamically."""
		...

	@overload
	def adjustPostRepStrengthDynamically(self, b : bool) -> None:
		"""Sets the option adjustPostRepStrengthDynamically tob."""
		...

	@overload
	def postSpringStrength(self) -> float:
		"""Returns the strength of the springs in the postprocessing step."""
		...

	@overload
	def postSpringStrength(self, x : float) -> None:
		"""Sets the strength of the springs in the postprocessing step tox."""
		...

	@overload
	def postStrengthOfRepForces(self) -> float:
		"""Returns the strength of the repulsive forces in the postprocessing step."""
		...

	@overload
	def postStrengthOfRepForces(self, x : float) -> None:
		"""Sets the strength of the repulsive forces in the postprocessing step tox."""
		...

	# Options for repulsive force approximation methods

	@overload
	def frGridQuotient(self) -> int:
		"""Returns the current setting of option frGridQuotient."""
		...

	@overload
	def frGridQuotient(self, p : int) -> None:
		"""Sets the option frGridQuotient top."""
		...

	@overload
	def nmTreeConstruction(self) -> FMMMOptions.ReducedTreeConstruction:
		"""Returns the current setting of option nmTreeConstruction."""
		...

	@overload
	def nmTreeConstruction(self, rtc : FMMMOptions.ReducedTreeConstruction) -> None:
		"""Sets the option nmTreeConstruction tortc."""
		...

	@overload
	def nmSmallCell(self) -> FMMMOptions.SmallestCellFinding:
		"""Returns the current setting of option nmSmallCell."""
		...

	@overload
	def nmSmallCell(self, scf : FMMMOptions.SmallestCellFinding) -> None:
		"""Sets the option nmSmallCell toscf."""
		...

	@overload
	def nmParticlesInLeaves(self) -> int:
		"""Returns the current setting of option nmParticlesInLeaves."""
		...

	@overload
	def nmParticlesInLeaves(self, n : int) -> None:
		"""Sets the option nmParticlesInLeaves ton."""
		...

	@overload
	def nmPrecision(self) -> int:
		"""Returns the precisionpfor thep-term multipole expansions."""
		...

	@overload
	def nmPrecision(self, p : int) -> None:
		"""Sets the precision for the multipole expansions top."""
		...

	# Most important functions

	# Functions for pre- and post-processing

	# Functions for divide et impera step

	# Functions for multilevel step

	# Functions for force calculation

	# Functions for analytic information

	def __init__(self) -> None:
		"""Creates an instance of the layout algorithm."""
		...

	def __destruct__(self) -> None:
		...

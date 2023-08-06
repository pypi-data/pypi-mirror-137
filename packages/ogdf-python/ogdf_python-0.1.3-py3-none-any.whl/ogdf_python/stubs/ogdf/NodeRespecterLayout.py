# file stubs/ogdf/NodeRespecterLayout.py generated from classogdf_1_1_node_respecter_layout
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class NodeRespecterLayout(ogdf.LayoutModule):

	"""TheNodeRespecterLayoutlayout algorithm."""

	# Setters for Algorithm Parameters

	def setRandomInitialPlacement(self, randomInitialPlacement : bool) -> None:
		"""Setsm_randomInitialPlacementtorandomInitialPlacement."""
		...

	def setPostProcessing(self, postProcessing : PostProcessingMode) -> None:
		"""Setsm_postProcessingtopostProcessing."""
		...

	def setBendNormalizationAngle(self, bendNormalizationAngle : float) -> None:
		"""Setsm_bendNormalizationAngletobendNormalizationAnglein [0...Pi]."""
		...

	def setNumberOfIterations(self, numberOfIterations : int) -> None:
		"""Setsm_numberOfIterationstonumberOfIterations>= 0."""
		...

	def setMinimalTemperature(self, minimalTemperature : float) -> None:
		"""Setsm_minimalTemperaturetominimalTemperature>= 0."""
		...

	def setInitialTemperature(self, initialTemperature : float) -> None:
		"""Setsm_initialTemperaturetoinitialTemperature>m_minimalTemperature."""
		...

	def setTemperatureDecreaseOffset(self, temperatureDecreaseOffset : float) -> None:
		"""Setsm_temperatureDecreaseOffsettotemperatureDecreaseOffsetin [0...1]."""
		...

	def setGravitation(self, gravitation : float) -> None:
		"""Setsm_gravitationtogravitation>= 0."""
		...

	def setOscillationAngle(self, oscillationAngle : float) -> None:
		"""Setsm_oscillationAngletooscillationAnglein [0...Pi]."""
		...

	def setDesiredMinEdgeLength(self, desiredMinEdgeLength : float) -> None:
		"""Setsm_desiredMinEdgeLengthtodesiredMinEdgeLength> 0."""
		...

	def setInitDummiesPerEdge(self, initDummiesPerEdge : int) -> None:
		"""Setsm_initDummiesPerEdgetoinitDummiesPerEdge>= 0."""
		...

	def setMaxDummiesPerEdge(self, maxDummiesPerEdge : int) -> None:
		"""Setsm_maxDummiesPerEdgetomaxDummiesPerEdge>m_initDummiesPerEdge."""
		...

	def setDummyInsertionThreshold(self, dummyInsertionThreshold : float) -> None:
		"""Setsm_dummyInsertionThresholdtodummyInsertionThreshold>= 1."""
		...

	def setMaxDisturbance(self, maxDisturbance : float) -> None:
		"""Setsm_maxDisturbancetomaxDisturbance>= 0."""
		...

	def setRepulsionDistance(self, repulsionDistance : float) -> None:
		"""Setsm_repulsionDistancetorepulsionDistance>= 0."""
		...

	def setMinDistCC(self, minDistCC : float) -> None:
		"""Setsm_minDistCCtominDistCC>= 0."""
		...

	def setPageRatio(self, pageRatio : float) -> None:
		"""Setsm_pageRatiotopageRatio> 0."""
		...

	# Getters for Algorithm Parameters

	def getRandomInitialPlacement(self) -> bool:
		"""Returnsm_randomInitialPlacement."""
		...

	def getPostProcessing(self) -> PostProcessingMode:
		"""Returnsm_postProcessing."""
		...

	def getBendNormalizationAngle(self) -> float:
		"""Returnsm_bendNormalizationAngle."""
		...

	def getNumberOfIterations(self) -> int:
		"""Returnsm_numberOfIterations."""
		...

	def getMinimalTemperature(self) -> float:
		"""Returnsm_minimalTemperature."""
		...

	def getInitialTemperature(self) -> float:
		"""Returnsm_initialTemperature."""
		...

	def getTemperatureDecreaseOffset(self) -> float:
		"""Returnsm_temperatureDecreaseOffset."""
		...

	def getGravitation(self) -> float:
		"""Returnsm_gravitation."""
		...

	def getOscillationAngle(self) -> float:
		"""Returnsm_oscillationAngle."""
		...

	def getDesiredMinEdgeLength(self) -> float:
		"""Returnsm_desiredMinEdgeLength."""
		...

	def getInitDummiesPerEdge(self) -> int:
		"""Returnsm_initDummiesPerEdge."""
		...

	def getMaxDummiesPerEdge(self) -> int:
		"""Returnsm_maxDummiesPerEdge."""
		...

	def getDummyInsertionThreshold(self) -> float:
		"""Returnsm_dummyInsertionThreshold."""
		...

	def getMaxDisturbance(self) -> float:
		"""Returnsm_maxDisturbance."""
		...

	def getRepulsionDistance(self) -> float:
		"""Returnsm_repulsionDistance."""
		...

	def getMinDistCC(self) -> float:
		"""Returnsm_minDistCC."""
		...

	def getPageRatio(self) -> float:
		"""Returnsm_pageRatio."""
		...

	# Algorithm Parameters

	# Graph Data Used by the Algorithm

	# Other Data Used by the Algorithm

	class PostProcessingMode(enum.Enum):

		"""Sets whether unnecessary edge bends should be filtered out in a post-processing step."""

		#: Keep all bends.
		_None = enum.auto()

		#: Activate post-processing but keep all bends on multi-edges and self-loops (such that the corresponding edges are visible).
		KeepMultiEdgeBends = enum.auto()

		#: Activate post-processing: Remove all bends that do not prevent edge-node intersections.
		Complete = enum.auto()

	def __init__(self) -> None:
		"""Creates an instance of theNodeRespecterLayout."""
		...

	def __destruct__(self) -> None:
		"""Destroys an instance of theNodeRespecterLayout."""
		...

	def call(self, attr : GraphAttributes) -> None:
		"""Calls the layout algorithm for theGraphAttributesattr."""
		...

# file stubs/ogdf/spring_embedder/SpringEmbedderBase.py generated from classogdf_1_1spring__embedder_1_1_spring_embedder_base
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class SpringEmbedderBase(ogdf.LayoutModule):

	"""Common base class for ogdf::SpringEmbedderBase andogdf::SpringEmbedderGridVariant."""

	class Scaling(enum.Enum):

		"""The scaling method used by the algorithm."""

		#: bounding box of input is used.
		input = enum.auto()

		#: bounding box set byuserBoundingBox()is used.
		userBoundingBox = enum.auto()

		#: automatic scaling is used with parameter set byscaleFunctionFactor()(larger factor, larger b-box).
		scaleFunction = enum.auto()

		#: use the given ideal edge length to scale the layout suitably.
		useIdealEdgeLength = enum.auto()

	#: convergence if avg.
	m_avgConvergenceFactor : float = ...

	m_boundingBox : DRect = ...

	m_coolDownFactor : float = ...

	m_forceLimitStep : float = ...

	m_forceModel : SpringForceModel = ...

	#: The used force model.
	m_forceModelImprove : SpringForceModel = ...

	#: The ideal edge length.
	m_idealEdgeLength : float = ...

	#: The number of iterations.
	m_iterations : int = ...

	#: The number of iterations for the improvement phase.
	m_iterationsImprove : int = ...

	#: convergence if max.
	m_maxConvergenceFactor : float = ...

	#: The maximal number of used threads.
	m_maxThreads : int = ...

	#: The minimal distance between connected components.
	m_minDistCC : float = ...

	#: The used force model for the improvement phase.
	m_noise : bool = ...

	#: The page ratio.
	m_pageRatio : float = ...

	#: The factor used if scaling type is scScaleFunction.
	m_scaleFactor : float = ...

	#: The scaling method.
	m_scaling : Scaling = ...

	m_userBoundingBox : DRect = ...

	def __init__(self) -> None:
		"""Constructor."""
		...

	@overload
	def avgConvergenceFactor(self) -> float:
		"""Returns the currently usedaverage convergence factor."""
		...

	@overload
	def avgConvergenceFactor(self, f : float) -> None:
		"""Sets theaverage convergence factortof."""
		...

	def call(self, GA : GraphAttributes) -> None:
		"""Computes a layout of graphGA."""
		...

	def coolDownFactor(self) -> float:
		...

	def forceLimitStep(self) -> float:
		...

	@overload
	def forceModel(self) -> SpringForceModel:
		"""Returns the currently used force model."""
		...

	@overload
	def forceModel(self, fm : SpringForceModel) -> None:
		"""Sets the used force model tofm."""
		...

	@overload
	def forceModelImprove(self) -> SpringForceModel:
		"""Returns the currently used force model for the improvement step."""
		...

	@overload
	def forceModelImprove(self, fm : SpringForceModel) -> None:
		"""Sets the used force model for the improvement step tofm."""
		...

	@overload
	def idealEdgeLength(self) -> float:
		"""Returns the current setting of ideal edge length."""
		...

	@overload
	def idealEdgeLength(self, len : float) -> None:
		"""Sets the ideal edge length tolen."""
		...

	@overload
	def iterations(self) -> int:
		"""Returns the current setting of iterations."""
		...

	@overload
	def iterations(self, i : int) -> None:
		"""Sets the number of iterations toi."""
		...

	@overload
	def iterationsImprove(self) -> int:
		"""Returns the current setting of iterations for the improvement phase."""
		...

	@overload
	def iterationsImprove(self, i : int) -> None:
		"""Sets the number of iterations for the improvement phase toi."""
		...

	@overload
	def maxConvergenceFactor(self) -> float:
		"""Returns the currently usedmaximumconvergence factor."""
		...

	@overload
	def maxConvergenceFactor(self, f : float) -> None:
		"""Sets themaximumconvergence factor tof."""
		...

	@overload
	def maxThreads(self) -> int:
		"""Returns the maximal number of used threads."""
		...

	@overload
	def maxThreads(self, n : int) -> None:
		"""Sets the maximal number of used threads ton."""
		...

	@overload
	def minDistCC(self) -> float:
		"""Returns the minimum distance between connected components."""
		...

	@overload
	def minDistCC(self, x : float) -> None:
		"""Sets the minimum distance between connected components tox."""
		...

	@overload
	def noise(self) -> bool:
		"""Returns the current setting of noise."""
		...

	@overload
	def noise(self, on : bool) -> None:
		"""Sets the parameter noise toon."""
		...

	@overload
	def pageRatio(self) -> float:
		"""Returns the page ratio."""
		...

	@overload
	def pageRatio(self, x : float) -> None:
		"""Sets the page ration tox."""
		...

	@overload
	def scaleFunctionFactor(self) -> float:
		"""Returns the current scale function factor."""
		...

	@overload
	def scaleFunctionFactor(self, f : float) -> None:
		"""Sets the scale function factor tof."""
		...

	@overload
	def scaling(self) -> Scaling:
		"""Returns the current scaling method."""
		...

	@overload
	def scaling(self, sc : Scaling) -> None:
		"""Sets the method for scaling the inital layout tosc."""
		...

	@overload
	def userBoundingBox(self) -> DRect:
		"""Gets the user bounding box."""
		...

	@overload
	def userBoundingBox(self, xmin : float, ymin : float, xmax : float, ymax : float) -> None:
		"""Sets the user bounding box (used if scaling method is scUserBoundingBox)."""
		...

	def callMaster(self, copy : GraphCopy, attr : GraphAttributes, box : DPoint) -> None:
		...

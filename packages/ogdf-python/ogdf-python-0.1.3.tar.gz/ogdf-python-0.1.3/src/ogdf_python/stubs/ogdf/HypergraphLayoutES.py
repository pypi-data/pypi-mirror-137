# file stubs/ogdf/HypergraphLayoutES.py generated from classogdf_1_1_hypergraph_layout_e_s
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class HypergraphLayoutES(ogdf.HypergraphLayoutModule):

	# Modules

	def setPlanarLayoutModule(self, pPlanarLayoutModule : LayoutPlanRepModule) -> None:
		"""Sets the module option for the planar layout."""
		...

	def setCrossingMinimizationModule(self, pCrossingMinimizationModule : CrossingMinimizationModule) -> None:
		"""Sets the module option for crossing minimization."""
		...

	def setEmbeddingModule(self, pEmbeddingModule : EmbedderModule) -> None:
		"""Sets the module option for embedding."""
		...

	class Profile(enum.Enum):

		"""Final appearance is driven by given profile."""

		Normal = enum.auto()

		ElectricCircuit = enum.auto()

	def __init__(self) -> None:
		...

	def __destruct__(self) -> None:
		...

	def call(self, HA : HypergraphAttributes) -> None:
		"""Computes a layout of hypergraph given byHA."""
		...

	def crossings(self) -> int:
		"""Returns the number of crossings in computed layout."""
		...

	def __assign__(self, hl : HypergraphLayoutES) -> HypergraphLayoutES:
		"""Assignment operator."""
		...

	def ratio(self) -> float:
		"""Returns the ratio between width and height of a drawing."""
		...

	def setConstraintIO(self, pConstraintIO : bool) -> None:
		"""Sets the Input / Output drawing requirement."""
		...

	def setProfile(self, pProfile : Profile) -> None:
		"""Sets the layout profile."""
		...

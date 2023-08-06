# file stubs/ogdf/GEMLayout.py generated from classogdf_1_1_g_e_m_layout
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class GEMLayout(ogdf.LayoutModule):

	"""The energy-based GEM layout algorithm."""

	@overload
	def __init__(self) -> None:
		"""Creates an instance of GEM layout."""
		...

	@overload
	def __init__(self, fl : GEMLayout) -> None:
		"""Copy constructor."""
		...

	def __destruct__(self) -> None:
		...

	@overload
	def attractionFormula(self) -> int:
		"""Returns the used formula for attraction (1 = Fruchterman / Reingold, 2 = GEM)."""
		...

	@overload
	def attractionFormula(self, n : int) -> None:
		"""sets the formula for attraction ton(1 = Fruchterman / Reingold, 2 = GEM)."""
		...

	def call(self, GA : GraphAttributes) -> None:
		"""Calls the layout algorithm for graph attributesGA."""
		...

	@overload
	def desiredLength(self) -> float:
		"""Returns the desired edge length."""
		...

	@overload
	def desiredLength(self, x : float) -> None:
		"""Sets the desired edge length tox; must be >= 0."""
		...

	@overload
	def gravitationalConstant(self) -> float:
		"""Returns the gravitational constant."""
		...

	@overload
	def gravitationalConstant(self, x : float) -> None:
		"""Sets the gravitational constant tox; must be >= 0. Attention! Only (very) small values give acceptable results."""
		...

	@overload
	def initialTemperature(self) -> float:
		"""Returns the initial temperature."""
		...

	@overload
	def initialTemperature(self, x : float) -> None:
		"""Sets the initial temperature tox; must be >= minimalTemperature."""
		...

	@overload
	def maximalDisturbance(self) -> float:
		"""Returns the maximal disturbance."""
		...

	@overload
	def maximalDisturbance(self, x : float) -> None:
		"""Sets the maximal disturbance tox; must be >= 0."""
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
	def minimalTemperature(self) -> float:
		"""Returns the minimal temperature."""
		...

	@overload
	def minimalTemperature(self, x : float) -> None:
		"""Sets the minimal temperature tox."""
		...

	@overload
	def numberOfRounds(self) -> int:
		"""Returns the maximal number of rounds per node."""
		...

	@overload
	def numberOfRounds(self, n : int) -> None:
		"""Sets the maximal number of round per node ton."""
		...

	def __assign__(self, fl : GEMLayout) -> GEMLayout:
		"""Assignment operator."""
		...

	@overload
	def oscillationAngle(self) -> float:
		"""Returns the opening angle for oscillations."""
		...

	@overload
	def oscillationAngle(self, x : float) -> None:
		"""Sets the opening angle for oscillations tox(0 <=x<= pi / 2)."""
		...

	@overload
	def oscillationSensitivity(self) -> float:
		"""Returns the oscillation sensitivity."""
		...

	@overload
	def oscillationSensitivity(self, x : float) -> None:
		"""Sets the oscillation sensitivity tox(0 <=x<= 1)."""
		...

	@overload
	def pageRatio(self) -> float:
		"""Returns the page ratio used for the layout of connected components."""
		...

	@overload
	def pageRatio(self, x : float) -> None:
		"""Sets the page ratio used for the layout of connected components tox."""
		...

	@overload
	def rotationAngle(self) -> float:
		"""Returns the opening angle for rotations."""
		...

	@overload
	def rotationAngle(self, x : float) -> None:
		"""Sets the opening angle for rotations tox(0 <=x<= pi / 2)."""
		...

	@overload
	def rotationSensitivity(self) -> float:
		"""Returns the rotation sensitivity."""
		...

	@overload
	def rotationSensitivity(self, x : float) -> None:
		"""Sets the rotation sensitivity tox(0 <=x<= 1)."""
		...

# file stubs/ogdf/UPRLayoutModule.py generated from classogdf_1_1_u_p_r_layout_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class UPRLayoutModule(object):

	"""Interface of hierarchy layout algorithms."""

	numberOfLevels : int = ...

	def __init__(self) -> None:
		"""Initializes a upward planarized representation layout module."""
		...

	def __destruct__(self) -> None:
		...

	def call(self, UPR : UpwardPlanRep, AG : GraphAttributes) -> None:
		"""Computes a upward layout ofUPRinAG."""
		...

	def doCall(self, UPR : UpwardPlanRep, AG : GraphAttributes) -> None:
		"""Implements the actual algorithm call."""
		...

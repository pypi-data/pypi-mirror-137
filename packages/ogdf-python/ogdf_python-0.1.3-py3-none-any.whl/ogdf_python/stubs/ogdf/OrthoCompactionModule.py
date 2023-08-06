# file stubs/ogdf/OrthoCompactionModule.py generated from classogdf_1_1_ortho_compaction_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class OrthoCompactionModule(ogdf.Module):

	def __init__(self) -> None:
		"""Constructs the compaction module."""
		...

	def __destruct__(self) -> None:
		"""Destroys the compaction module."""
		...

	def callConstructive(self, PG : PlanRep, OR : OrthoRep, drawing : GridLayout) -> None:
		"""call to construct a drawing for an orthogonal representationORofPlanRepPG. Has to be implemented by derived classes."""
		...

	def callImprovement(self, PG : PlanRep, OR : OrthoRep, drawing : GridLayout) -> None:
		"""call to improve a given orthogonal drawingdrawing. Has to be implemented by derived classes."""
		...

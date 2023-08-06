# file stubs/ogdf/MultiEdgeApproxInserter/__init__.py generated from classogdf_1_1_multi_edge_approx_inserter
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class MultiEdgeApproxInserter(ogdf.EdgeInsertionModule):

	"""Multi edge inserter with approximation guarantee."""

	@overload
	def __init__(self) -> None:
		"""Creates an instance of multi-edge approx inserter with default option settings."""
		...

	@overload
	def __init__(self, inserter : MultiEdgeApproxInserter) -> None:
		"""Creates an instance of multi-edge approx inserter with the same settings asinserter."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...

	def clone(self) -> EdgeInsertionModule:
		"""Returns a new instance of the multi-edge approx inserter with the same option settings."""
		...

	def __assign__(self, inserter : MultiEdgeApproxInserter) -> MultiEdgeApproxInserter:
		"""Assignment operator. Copies option settings only."""
		...

	@overload
	def percentMostCrossedFix(self) -> float:
		"""Returns the current setting of option percentMostCrossed."""
		...

	@overload
	def percentMostCrossedFix(self, percent : float) -> None:
		"""Sets the optionpercentMostCrossedtopercent."""
		...

	@overload
	def percentMostCrossedVar(self) -> float:
		"""Returns the current setting of option percentMostCrossed (variable embedding)."""
		...

	@overload
	def percentMostCrossedVar(self, percent : float) -> None:
		"""Sets the optionpercentMostCrossedVartopercent."""
		...

	@overload
	def removeReinsertFix(self) -> RemoveReinsertType:
		"""Returns the current setting of the remove-reinsert postprocessing method."""
		...

	@overload
	def removeReinsertFix(self, rrOption : RemoveReinsertType) -> None:
		"""Sets the remove-reinsert postprocessing method."""
		...

	@overload
	def removeReinsertVar(self) -> RemoveReinsertType:
		"""Returns the current setting of the remove-reinsert postprocessing method."""
		...

	@overload
	def removeReinsertVar(self, rrOption : RemoveReinsertType) -> None:
		"""Sets the remove-reinsert postprocessing method."""
		...

	@overload
	def statistics(self) -> bool:
		...

	@overload
	def statistics(self, b : bool) -> None:
		...

	def sumFEInsertionCosts(self) -> int:
		...

	def sumInsertionCosts(self) -> int:
		...

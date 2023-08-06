# file stubs/ogdf/FixedEmbeddingInserter.py generated from classogdf_1_1_fixed_embedding_inserter
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class FixedEmbeddingInserter(ogdf.EdgeInsertionModule):

	"""Inserts edges optimally into an embedding."""

	# Optional parameters

	@overload
	def removeReinsert(self, rrOption : RemoveReinsertType) -> None:
		"""Sets the remove-reinsert postprocessing method."""
		...

	@overload
	def removeReinsert(self) -> RemoveReinsertType:
		"""Returns the current setting of the remove-reinsert postprocessing method."""
		...

	@overload
	def percentMostCrossed(self, percent : float) -> None:
		"""Sets the optionpercentMostCrossedtopercent."""
		...

	@overload
	def percentMostCrossed(self) -> float:
		"""Returns the current setting of option percentMostCrossed."""
		...

	def keepEmbedding(self, keep : bool) -> None:
		"""Sets the optionkeepEmbeddingtokeep."""
		...

	def keepEmbeding(self) -> bool:
		"""Returns the current setting of optionkeepEmbedding."""
		...

	# Further information

	def runsPostprocessing(self) -> int:
		"""Returns the number of runs performed by the remove-reinsert method after the algorithm has been called."""
		...

	@overload
	def __init__(self) -> None:
		"""Creates an instance of fixed embedding edge inserter with default settings."""
		...

	@overload
	def __init__(self, inserter : FixedEmbeddingInserter) -> None:
		"""Creates an instance of fixed embedding edge inserter with the same settings asinserter."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...

	def clone(self) -> EdgeInsertionModule:
		"""Returns a new instance of the fixed embedding inserter with the same option settings."""
		...

	def __assign__(self, inserter : FixedEmbeddingInserter) -> FixedEmbeddingInserter:
		"""Assignment operator. Copies option settings only."""
		...

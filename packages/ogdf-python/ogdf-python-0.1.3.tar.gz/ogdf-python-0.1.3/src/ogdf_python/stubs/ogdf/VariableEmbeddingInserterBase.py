# file stubs/ogdf/VariableEmbeddingInserterBase.py generated from classogdf_1_1_variable_embedding_inserter_base
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class VariableEmbeddingInserterBase(ogdf.EdgeInsertionModule):

	"""Common parameter functionality forogdf::VariableEmbeddingInserterandogdf::VariableEmbeddingInserterDyn."""

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

	# Further information

	@overload
	def runsPostprocessing(self) -> int:
		"""Returns the number of runs performed by the remove-reinsert method after the algorithm has been called."""
		...

	@overload
	def runsPostprocessing(self, runs : int) -> None:
		"""Sets the number of runs performed by the remove-reinsert method."""
		...

	@overload
	def __init__(self) -> None:
		"""Creates an instance of variable embedding edge inserter with default settings."""
		...

	@overload
	def __init__(self, inserter : VariableEmbeddingInserterBase) -> None:
		"""Creates an instance of variable embedding inserter with the same settings asinserter."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...

	def __assign__(self, inserter : VariableEmbeddingInserterBase) -> VariableEmbeddingInserterBase:
		"""Assignment operator. Copies option settings only."""
		...

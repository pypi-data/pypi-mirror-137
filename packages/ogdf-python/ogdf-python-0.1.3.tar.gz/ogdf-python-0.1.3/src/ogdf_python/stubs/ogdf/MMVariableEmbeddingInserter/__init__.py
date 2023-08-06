# file stubs/ogdf/MMVariableEmbeddingInserter/__init__.py generated from classogdf_1_1_m_m_variable_embedding_inserter
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class MMVariableEmbeddingInserter(ogdf.MMEdgeInsertionModule):

	"""Minor-monotone edge insertion with variable embedding."""

	def __init__(self) -> None:
		"""Creates a minor-monotone fixed embedding inserter."""
		...

	def __destruct__(self) -> None:
		...

	@overload
	def percentMostCrossed(self) -> float:
		"""Returns the current setting of the option percentMostCrossed."""
		...

	@overload
	def percentMostCrossed(self, percent : float) -> None:
		"""Sets the portion of most crossed edges used during postprocessing."""
		...

	@overload
	def removeReinsert(self) -> RemoveReinsertType:
		"""Returns the current setting of the remove-reinsert option."""
		...

	@overload
	def removeReinsert(self, rrOption : RemoveReinsertType) -> None:
		"""Sets the remove-reinsert option for postprocessing."""
		...

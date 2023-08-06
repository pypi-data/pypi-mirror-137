# file stubs/ogdf/FixedEmbeddingInserterUML.py generated from classogdf_1_1_fixed_embedding_inserter_u_m_l
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class FixedEmbeddingInserterUML(ogdf.UMLEdgeInsertionModule):

	"""Edge insertion module that inserts each edge optimally into a fixed embedding."""

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

	@overload
	def __init__(self) -> None:
		"""Creates an instance of variable embedding edge inserter with default settings."""
		...

	@overload
	def __init__(self, inserter : FixedEmbeddingInserterUML) -> None:
		"""Creates an instance of fixed embedding edge inserter with the same settings asinserter."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...

	def clone(self) -> UMLEdgeInsertionModule:
		"""Returns a new instance of the fixed embedding inserter with the same option settings."""
		...

	def __assign__(self, inserter : FixedEmbeddingInserterUML) -> FixedEmbeddingInserterUML:
		"""Assignment operator. Copies option settings only."""
		...

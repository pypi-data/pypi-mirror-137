# file stubs/ogdf/VariableEmbeddingInserterUML.py generated from classogdf_1_1_variable_embedding_inserter_u_m_l
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class VariableEmbeddingInserterUML(ogdf.UMLEdgeInsertionModule):

	"""Optimal edge insertion module."""

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

	@overload
	def __init__(self) -> None:
		"""Creates an instance of variable embedding edge inserter with default settings."""
		...

	@overload
	def __init__(self, inserter : VariableEmbeddingInserterUML) -> None:
		"""Creates an instance of variable embedding inserter with the same settings asinserter."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...

	def clone(self) -> UMLEdgeInsertionModule:
		"""Returns a new instance of the variable embedding inserter with the same option settings."""
		...

	def __assign__(self, inserter : VariableEmbeddingInserterUML) -> VariableEmbeddingInserterUML:
		"""Assignment operator. Copies option settings only."""
		...

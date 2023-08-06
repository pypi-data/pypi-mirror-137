# file stubs/ogdf/VariableEmbeddingInserterDyn.py generated from classogdf_1_1_variable_embedding_inserter_dyn
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class VariableEmbeddingInserterDyn(ogdf.VariableEmbeddingInserterBase):

	"""Optimal edge insertion module."""

	def clone(self) -> EdgeInsertionModule:
		"""Returns a new instance of the variable embedding inserter with the same option settings."""
		...

	@overload
	def VariableEmbeddingInserterBase(self) -> None:
		"""Creates an instance of variable embedding edge inserter with default settings."""
		...

	@overload
	def VariableEmbeddingInserterBase(self, inserter : VariableEmbeddingInserterBase) -> None:
		"""Creates an instance of variable embedding inserter with the same settings asinserter."""
		...

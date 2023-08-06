# file stubs/ogdf/VariableEmbeddingInserter.py generated from classogdf_1_1_variable_embedding_inserter
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class VariableEmbeddingInserter(ogdf.VariableEmbeddingInserterBase):

	"""Optimal edge insertion module."""

	def callPostprocessing(self, pr : PlanRepLight, origEdges : Array[edge]) -> Module.ReturnType:
		"""Calls only the postprocessing; assumes that all edges inorigEdgesare already inserted intopr."""
		...

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

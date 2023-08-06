# file stubs/ogdf/Module.py generated from classogdf_1_1_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Module(object):

	"""Base class for modules."""

	class ReturnType(enum.Enum):

		"""The return type of a module."""

		#: The solution is feasible.
		Feasible = enum.auto()

		#: The solution is optimal.
		Optimal = enum.auto()

		#: There exists no feasible solution.
		NoFeasibleSolution = enum.auto()

		#: The solution is feasible, but there was a timeout.
		TimeoutFeasible = enum.auto()

		#: The solution is not feasible due to a timeout.
		TimeoutInfeasible = enum.auto()

		#: Computation was aborted due to an error.
		Error = enum.auto()

	def __init__(self) -> None:
		"""Initializes a module."""
		...

	def __destruct__(self) -> None:
		...

	def isSolution(self, ret : ReturnType) -> bool:
		"""Returns true iffretindicates that the module returned a feasible solution."""
		...

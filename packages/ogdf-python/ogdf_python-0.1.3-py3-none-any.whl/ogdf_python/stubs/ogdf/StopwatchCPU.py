# file stubs/ogdf/StopwatchCPU.py generated from classogdf_1_1_stopwatch_c_p_u
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class StopwatchCPU(ogdf.Stopwatch):

	"""Implements a stopwatch measuring CPU time."""

	@overload
	def __init__(self) -> None:
		"""Creates a stopwatch for measuring CPU time with total time 0."""
		...

	@overload
	def __init__(self, milliSecs : int) -> None:
		"""Creates a stopwatch for measuring CPU time and sets its total time tomilliSecs."""
		...

	def __destruct__(self) -> None:
		...

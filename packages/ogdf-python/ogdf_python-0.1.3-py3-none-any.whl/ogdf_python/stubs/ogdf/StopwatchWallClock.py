# file stubs/ogdf/StopwatchWallClock.py generated from classogdf_1_1_stopwatch_wall_clock
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class StopwatchWallClock(ogdf.Stopwatch):

	"""Implements a stopwatch measuring wall-clock time."""

	@overload
	def __init__(self) -> None:
		"""Creates a stopwatch for measuring wall-clock time with total time 0."""
		...

	@overload
	def __init__(self, milliSecs : int) -> None:
		"""Creates a stopwatch for measuring wall-clock time and sets its total time tomilliSecs."""
		...

	def __destruct__(self) -> None:
		...

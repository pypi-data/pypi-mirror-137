# file stubs/ogdf/Stopwatch.py generated from classogdf_1_1_stopwatch
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Stopwatch(object):

	"""Realizes a stopwatch for measuring elapsed time."""

	@overload
	def __init__(self) -> None:
		"""Initializes a stop watch with total time 0."""
		...

	@overload
	def __init__(self, milliSecs : int) -> None:
		"""Initializes a stopwatch and sets its total time tomilliSecs."""
		...

	def __destruct__(self) -> None:
		...

	def addCentiSeconds(self, centiSeconds : int) -> None:
		"""AddscentiSecondsto total time."""
		...

	def centiSeconds(self) -> int:
		"""Returns the currently elapsed time in 1/100-seconds."""
		...

	def exceeds(self, maxSeconds : int) -> bool:
		"""Returns true iff the currently elapsed time exceedsmaxSeconds."""
		...

	def hours(self) -> int:
		"""Returns the currently elapsed time in hours."""
		...

	def milliSeconds(self) -> int:
		"""Returns the currently elapsed time in milliseconds."""
		...

	def minutes(self) -> int:
		"""Returns the currently elapsed time in minutes."""
		...

	def reset(self) -> None:
		"""Stops the stopwatch and sets its total time to 0."""
		...

	def running(self) -> bool:
		"""Returns true if the stopwatch is running, false otherwise."""
		...

	def seconds(self) -> int:
		"""Returns the currently elapsed time in seconds."""
		...

	def start(self, reset : bool = False) -> None:
		"""Starts the stopwatch."""
		...

	def stop(self) -> None:
		"""Stops the stopwatch and adds the difference between the current time and the starting time to the total time."""
		...

	def theTime(self) -> int:
		"""Returns the current time in milliseconds (from some fixed starting point)."""
		...

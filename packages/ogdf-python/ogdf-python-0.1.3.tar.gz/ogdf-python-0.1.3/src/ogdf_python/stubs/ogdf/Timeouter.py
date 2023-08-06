# file stubs/ogdf/Timeouter.py generated from classogdf_1_1_timeouter
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Timeouter(object):

	"""class for timeout funtionality."""

	#: Time limit for module calls (< 0 means no limit).
	m_timeLimit : float = ...

	@overload
	def __init__(self) -> None:
		"""timeout is turned of by default"""
		...

	@overload
	def __init__(self, t : bool) -> None:
		"""timeout is turned off (false) or on (true) (with 0 second)"""
		...

	@overload
	def __init__(self, t : Timeouter) -> None:
		...

	@overload
	def __init__(self, t : float) -> None:
		"""timeout is set to the given value (seconds)"""
		...

	def __destruct__(self) -> None:
		...

	def isTimeLimit(self) -> bool:
		"""returns whether any time limit is set or not"""
		...

	def __assign__(self, t : Timeouter) -> Timeouter:
		...

	@overload
	def timeLimit(self) -> float:
		"""returns the current time limit for the call"""
		...

	@overload
	def timeLimit(self, t : bool) -> None:
		"""shorthand to turn timelimit off or on (with 0 seconds)"""
		...

	@overload
	def timeLimit(self, t : float) -> None:
		"""sets the time limit for the call (in seconds); <0 means no limit."""
		...

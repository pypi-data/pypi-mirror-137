# file stubs/ogdf/Thread.py generated from classogdf_1_1_thread
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
Function = TypeVar('Function')

Args = TypeVar('Args')

class Thread(thread):

	"""Threads supporting OGDF's memory management."""

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, f : Function, args : Args) -> None:
		...

	@overload
	def __init__(self, other : Thread) -> None:
		...

	def __assign__(self, other : Thread) -> Thread:
		...

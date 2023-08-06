# file stubs/ogdf/Barrier.py generated from classogdf_1_1_barrier
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Barrier(object):

	"""Representation of a barrier."""

	def __init__(self, numThreads : int) -> None:
		"""Creates a barrier for a group ofnumThreadsthreads."""
		...

	def threadSync(self) -> None:
		"""Synchronizes the threads in the group."""
		...

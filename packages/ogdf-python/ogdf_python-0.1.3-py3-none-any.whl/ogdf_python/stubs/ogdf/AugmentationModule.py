# file stubs/ogdf/AugmentationModule.py generated from classogdf_1_1_augmentation_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class AugmentationModule(object):

	"""The base class for graph augmentation algorithms."""

	def __init__(self) -> None:
		"""Initializes an augmentation module."""
		...

	def __destruct__(self) -> None:
		...

	@overload
	def call(self, G : Graph) -> None:
		"""Calls the augmentation module for graphG."""
		...

	@overload
	def call(self, G : Graph, L : List[edge]) -> None:
		"""Calls the augmentation module for graphG."""
		...

	def numberOfAddedEdges(self) -> int:
		"""Returns the number of added edges."""
		...

	@overload
	def __call__(self, G : Graph) -> None:
		"""Calls the augmentation module for graphG."""
		...

	@overload
	def __call__(self, G : Graph, L : List[edge]) -> None:
		"""Calls the augmentation module for graphG."""
		...

	def doCall(self, G : Graph, L : List[edge]) -> None:
		"""Implements the augmentation algorithm for graphG."""
		...

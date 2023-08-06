# file stubs/ogdf/steiner_tree/LossMetadata.py generated from structogdf_1_1steiner__tree_1_1_loss_metadata
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class LossMetadata(Generic[T]):

	#: Listof non-loss edges.
	bridges : List[edge] = ...

	#: The loss of a component.
	loss : T = ...

	def __init__(self) -> None:
		...

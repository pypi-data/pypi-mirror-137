# file stubs/ogdf/KuratowskiWrapper.py generated from classogdf_1_1_kuratowski_wrapper
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class KuratowskiWrapper(object):

	"""Wrapper-class for Kuratowski Subdivisions containing the minortype and edgelist."""

	class SubdivisionType(enum.Enum):

		"""Possible minortypes of a Kuratowski Subdivision."""

		A = enum.auto()

		AB = enum.auto()

		AC = enum.auto()

		AD = enum.auto()

		AE1 = enum.auto()

		AE2 = enum.auto()

		AE3 = enum.auto()

		AE4 = enum.auto()

		B = enum.auto()

		C = enum.auto()

		D = enum.auto()

		E1 = enum.auto()

		E2 = enum.auto()

		E3 = enum.auto()

		E4 = enum.auto()

		E5 = enum.auto()

	#: Contains the edges of the Kuratowski Subdivision.
	edgeList : SListPure[edge] = ...

	#: Minortype of the Kuratowski Subdivision.
	subdivisionType : SubdivisionType = ...

	#: The node which was embedded while the Kuratowski Subdivision was found.
	V : node = ...

	def __init__(self) -> None:
		"""Constructor."""
		...

	def isK33(self) -> bool:
		"""Returns true, iff subdivision is a K3,3-minor."""
		...

	def isK5(self) -> bool:
		"""Returns true, iff subdivision is a K5-minor."""
		...

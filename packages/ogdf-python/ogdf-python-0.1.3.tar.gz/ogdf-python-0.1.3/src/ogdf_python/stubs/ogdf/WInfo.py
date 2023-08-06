# file stubs/ogdf/WInfo.py generated from structogdf_1_1_w_info
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class WInfo(object):

	"""Saves information about a pertinent node w between two stopping vertices."""

	class MinorType(enum.Enum):

		"""All possible base minortypes on w."""

		A = enum.auto()

		B = enum.auto()

		C = enum.auto()

		D = enum.auto()

		E = enum.auto()

	externEEnd : SListIterator[ExternE] = ...

	externEStart : SListIterator[ExternE] = ...

	firstExternEAfterW : node = ...

	highestXYPath : ArrayBuffer[adjEntry] = ...

	minorType : int = ...

	pertinentPaths : SListPure[SListPure[edge] ] = ...

	pxAboveStopX : bool = ...

	pyAboveStopY : bool = ...

	w : node = ...

	zPath : ArrayBuffer[adjEntry] = ...

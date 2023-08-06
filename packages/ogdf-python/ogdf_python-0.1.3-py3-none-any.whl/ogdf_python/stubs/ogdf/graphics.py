# file stubs/ogdf/graphics.py generated from namespaceogdf_1_1graphics
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
ToClass = TypeVar('ToClass')

FromClass = TypeVar('FromClass')

Enum = TypeVar('Enum')

class graphics(object):

	fromFillPattern : Dict[FillPattern, str ] = ...

	fromShape : Dict[Shape, str ] = ...

	fromStrokeType : Dict[StrokeType, str ] = ...

	toFillPattern : Dict[ str,FillPattern] = ...

	toShape : Dict[ str,Shape] = ...

	toStrokeType : Dict[ str,StrokeType] = ...

	@overload
	def getMapToEnum(self) -> Dict[ str, ToClass ]:
		...

	@overload
	def getMapToEnum(self) -> Dict[ str,FillPattern]:
		...

	@overload
	def getMapToString(self) -> Dict[ FromClass, str ]:
		...

	@overload
	def getMapToString(self) -> Dict[FillPattern, str ]:
		...

	def init(self) -> None:
		...

	def initFillPattern(self) -> None:
		...

	def initShape(self) -> None:
		...

	def initStrokeType(self) -> None:
		...

	def initSecondMap(self, fromMap : Dict[ Enum, str ], toMap : Dict[ str, Enum ]) -> None:
		...

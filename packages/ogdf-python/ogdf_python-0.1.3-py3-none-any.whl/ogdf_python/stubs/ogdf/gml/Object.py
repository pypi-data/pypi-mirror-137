# file stubs/ogdf/gml/Object.py generated from structogdf_1_1gml_1_1_object
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Object(object):

	"""Represents node in GML parse tree."""

	_ : WTF_TYPE["union ogdf.gml.Object.@2"] = ...

	doubleValue : float = ...

	intValue : int = ...

	key : Key = ...

	pBrother : Object = ...

	pFirstSon : Object = ...

	stringValue : str = ...

	valueType : ObjectType = ...

	@overload
	def __init__(self, k : Key) -> None:
		...

	@overload
	def __init__(self, k : Key, value : str) -> None:
		...

	@overload
	def __init__(self, k : Key, value : float) -> None:
		...

	@overload
	def __init__(self, k : Key, value : int) -> None:
		...

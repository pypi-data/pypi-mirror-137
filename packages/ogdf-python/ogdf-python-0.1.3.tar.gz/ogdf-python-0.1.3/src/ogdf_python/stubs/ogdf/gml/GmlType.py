# file stubs/ogdf/gml/GmlType.py generated from structogdf_1_1gml_1_1_gml_type
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class GmlType(Generic[T]):

	type : ObjectType = ...

	@overload
	def get_attr(self, _ : Object) -> T:
		...

	@overload
	def get_attr(self, obj : Object) -> int:
		...

	@overload
	def get_attr(self, obj : Object) -> float:
		...

	@overload
	def get_attr(self, obj : Object) -> str:
		...

	@overload
	def type(self) -> ObjectType:
		...

	@overload
	def type(self) -> ObjectType:
		...

	@overload
	def type(self) -> ObjectType:
		...

# file stubs/ogdf/tlp/Token.py generated from structogdf_1_1tlp_1_1_token
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Token(object):

	class Type(enum.Enum):

		leftParen = enum.auto()

		rightParen = enum.auto()

		identifier = enum.auto()

		string = enum.auto()

	column : size_t = ...

	line : size_t = ...

	type : enumogdf.tlp.Token.Type = ...

	value : str = ...

	def __init__(self, type : Type, line : size_t, column : size_t) -> None:
		...

	@overload
	def identifier(self) -> bool:
		...

	@overload
	def identifier(self, str : str) -> bool:
		...

	def leftParen(self) -> bool:
		...

	def rightParen(self) -> bool:
		...

	@overload
	def string(self) -> bool:
		...

	@overload
	def string(self, str : str) -> bool:
		...

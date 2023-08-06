# file stubs/ogdf/tlp/Lexer.py generated from classogdf_1_1tlp_1_1_lexer
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Lexer(object):

	def __init__(self, _is : std.istream) -> None:
		...

	def __destruct__(self) -> None:
		...

	def tokenize(self) -> bool:
		...

	def tokens(self) -> List[Token]:
		...

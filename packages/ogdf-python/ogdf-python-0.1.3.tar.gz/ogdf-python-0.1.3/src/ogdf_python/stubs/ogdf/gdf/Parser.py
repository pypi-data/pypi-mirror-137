# file stubs/ogdf/gdf/Parser.py generated from classogdf_1_1gdf_1_1_parser
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Parser(object):

	def __init__(self, _is : std.istream) -> None:
		...

	@overload
	def read(self, G : Graph) -> bool:
		...

	@overload
	def read(self, G : Graph, GA : GraphAttributes) -> bool:
		...

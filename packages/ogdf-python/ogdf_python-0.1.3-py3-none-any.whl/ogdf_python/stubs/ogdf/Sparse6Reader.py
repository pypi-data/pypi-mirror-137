# file stubs/ogdf/Sparse6Reader.py generated from classogdf_1_1_sparse6_reader
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Sparse6Reader(ogdf.G6AbstractReader[ Sparse6Implementation ]):

	def __init__(self, G : Graph, _is : std.istream, forceHeader : bool) -> None:
		...

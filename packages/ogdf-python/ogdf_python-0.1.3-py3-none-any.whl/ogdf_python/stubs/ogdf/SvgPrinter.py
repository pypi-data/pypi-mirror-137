# file stubs/ogdf/SvgPrinter.py generated from classogdf_1_1_svg_printer
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class SvgPrinter(object):

	"""SVG Writer."""

	@overload
	def __init__(self, attr : ClusterGraphAttributes, settings : GraphIO.SVGSettings) -> None:
		"""Creates a new SVG Printer for aogdf::ClusterGraph."""
		...

	@overload
	def __init__(self, attr : GraphAttributes, settings : GraphIO.SVGSettings) -> None:
		"""Creates a new SVG Printer for aogdf::Graph."""
		...

	def draw(self, os : std.ostream) -> bool:
		"""Prints the graph and attributes of this printer to the given output stream."""
		...

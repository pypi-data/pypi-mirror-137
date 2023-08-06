# file stubs/ogdf/ComponentSplitterLayout.py generated from classogdf_1_1_component_splitter_layout
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ComponentSplitterLayout(ogdf.LayoutModule):

	def __init__(self) -> None:
		...

	def call(self, GA : GraphAttributes) -> None:
		"""Computes a layout of graphGA."""
		...

	def setBorder(self, border : int) -> None:
		...

	def setLayoutModule(self, layout : LayoutModule) -> None:
		...

	def setPacker(self, packer : CCLayoutPackModule) -> None:
		...

# file stubs/ogdf/SpringEmbedderGridVariant/__init__.py generated from classogdf_1_1_spring_embedder_grid_variant
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class SpringEmbedderGridVariant(ogdf.spring_embedder.SpringEmbedderBase):

	"""The spring-embedder layout algorithm with force approximation using hte grid variant approach."""

	def __init__(self) -> None:
		...

	def callMaster(self, copy : GraphCopy, attr : GraphAttributes, box : DPoint) -> None:
		...

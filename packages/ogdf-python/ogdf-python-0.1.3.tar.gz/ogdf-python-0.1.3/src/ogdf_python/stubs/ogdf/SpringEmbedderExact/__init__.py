# file stubs/ogdf/SpringEmbedderExact/__init__.py generated from classogdf_1_1_spring_embedder_exact
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class SpringEmbedderExact(ogdf.spring_embedder.SpringEmbedderBase):

	"""The spring-embedder layout algorithm with exact computation of forces."""

	def __init__(self) -> None:
		...

	def callMaster(self, copy : GraphCopy, attr : GraphAttributes, box : DPoint) -> None:
		...

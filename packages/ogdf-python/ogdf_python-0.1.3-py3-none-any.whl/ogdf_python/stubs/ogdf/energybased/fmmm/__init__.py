# file stubs/ogdf/energybased/fmmm/__init__.py generated from namespaceogdf_1_1energybased_1_1fmmm
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class fmmm(object):

	def calculate_forces_inside_contained_nodes(self, F_rep : NodeArray[DPoint], A : NodeArray[NodeAttributes], contained_nodes : List[node]) -> None:
		...

	def log(self, z : complex[ float ]) -> complex[ float ]:
		...

	def OGDF_DECLARE_COMPARER(self, _ : ParticleInfoComparer, _ : ParticleInfo, _ : float, get_x_y_coord : WTF_TYPE["x."]) -> None:
		...

	@overload
	def __lshift__(self, output : std.ostream, A : EdgeAttributes) -> std.ostream:
		...

	@overload
	def __lshift__(self, output : std.ostream, A : NodeAttributes) -> std.ostream:
		...

	@overload
	def __lshift__(self, output : std.ostream, A : QuadTreeNodeNM) -> std.ostream:
		...

	@overload
	def __rshift__(self, input : std.istream, A : EdgeAttributes) -> std.istream:
		...

	@overload
	def __rshift__(self, input : std.istream, _ : NodeAttributes) -> std.istream:
		...

	@overload
	def __rshift__(self, input : std.istream, A : QuadTreeNodeNM) -> std.istream:
		...

	def random_precision_number(self, shift : float) -> float:
		...

	def traverse(self, relevantList : List[ParticleInfo], mid_coord : float) -> ParticleListState:
		...

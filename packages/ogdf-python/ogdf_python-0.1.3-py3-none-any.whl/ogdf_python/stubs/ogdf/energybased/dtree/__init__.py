# file stubs/ogdf/energybased/dtree/__init__.py generated from namespaceogdf_1_1energybased_1_1dtree
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
Dim = TypeVar('Dim')

IntType = TypeVar('IntType')

K = TypeVar('K')

class dtree(object):

	DTreeEmbedder2D : Type = DTreeEmbedder[ 2 ]

	DTreeEmbedder3D : Type = DTreeEmbedder[ 3 ]

	def AttrForceFunctionLog(self, dist : float, force : float, force_prime : float) -> None:
		...

	@overload
	def AttrForceFunctionPow(self, dist : float, force : float, force_prime : float) -> Annotated[ None , "std.enable_if[ Dim !=2||(K !=1 K !=2), None ].type"]:
		...

	@overload
	def AttrForceFunctionPow(self, dist : float, force : float, force_prime : float) -> Annotated[ None , "std.enable_if[ Dim==2 K==2, None ].type"]:
		...

	@overload
	def AttrForceFunctionPow(self, dist : float, force : float, force_prime : float) -> Annotated[ None , "std.enable_if[ Dim==2 K==1, None ].type"]:
		...

	@overload
	def computeDeltaAndDistance(self, a : float, b : float, delta : float) -> Annotated[ float , "std.enable_if[ Dim !=2, float ].type"]:
		...

	@overload
	def computeDeltaAndDistance(self, a : float, b : float, delta : float) -> Annotated[ float , "std.enable_if[ Dim==2, float ].type"]:
		...

	@overload
	def interleaveBits(self, coords : IntType, mnr : IntType) -> Annotated[ None , "std.enable_if[ Dim !=1 Dim !=2, None ].type"]:
		...

	@overload
	def interleaveBits(self, coords : int, mnr : int) -> Annotated[ None , "std.enable_if[ Dim==1, None ].type"]:
		...

	@overload
	def interleaveBits(self, coords : int, mnr : int) -> Annotated[ None , "std.enable_if[ Dim==2, None ].type"]:
		...

	@overload
	def lowestCommonAncestorLevel(self, a : IntType, b : IntType) -> Annotated[  int , "std.enable_if[ Dim !=1,  int ].type"]:
		...

	@overload
	def lowestCommonAncestorLevel(self, a : int, b : int) -> Annotated[  int , "std.enable_if[ Dim==1,  int ].type"]:
		...

	@overload
	def mortonComparerEqual(self, a : IntType, b : IntType) -> Annotated[ bool , "std.enable_if[ Dim !=1 Dim !=2, bool ].type"]:
		...

	@overload
	def mortonComparerEqual(self, a : IntType, b : IntType) -> Annotated[ bool , "std.enable_if[ Dim==1, bool ].type"]:
		...

	@overload
	def mortonComparerEqual(self, a : IntType, b : IntType) -> Annotated[ bool , "std.enable_if[ Dim==2, bool ].type"]:
		...

	@overload
	def mortonComparerLess(self, a : IntType, b : IntType) -> Annotated[ bool , "std.enable_if[ Dim !=1 Dim !=2, bool ].type"]:
		...

	@overload
	def mortonComparerLess(self, a : int, b : int) -> Annotated[ bool , "std.enable_if[ Dim==1, bool ].type"]:
		...

	@overload
	def mortonComparerLess(self, a : int, b : int) -> Annotated[ bool , "std.enable_if[ Dim==2, bool ].type"]:
		...

	def mostSignificantBit(self, x : IntType) -> int:
		...

	@overload
	def RepForceFunctionNewton(self, dist : float, force : float, force_prime : float) -> Annotated[ None , "std.enable_if[ Dim !=2||(K !=1 K !=2), None ].type"]:
		...

	@overload
	def RepForceFunctionNewton(self, dist : float, force : float, force_prime : float) -> Annotated[ None , "std.enable_if[ Dim==2 K==2, None ].type"]:
		...

	@overload
	def RepForceFunctionNewton(self, dist : float, force : float, force_prime : float) -> Annotated[ None , "std.enable_if[ Dim==2 K==1, None ].type"]:
		...

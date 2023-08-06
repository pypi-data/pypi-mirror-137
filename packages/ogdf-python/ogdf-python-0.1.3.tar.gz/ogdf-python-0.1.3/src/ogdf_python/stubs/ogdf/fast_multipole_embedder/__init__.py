# file stubs/ogdf/fast_multipole_embedder/__init__.py generated from namespaceogdf_1_1fast__multipole__embedder
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
FuncFirst = TypeVar('FuncFirst')

C_T = TypeVar('C_T')

ArgType6 = TypeVar('ArgType6')

MNR_T = TypeVar('MNR_T')

ArgType2 = TypeVar('ArgType2')

FLAGS = TypeVar('FLAGS')

CondType = TypeVar('CondType')

ArgType3 = TypeVar('ArgType3')

ArgType8 = TypeVar('ArgType8')

F = TypeVar('F')

FunctionType = TypeVar('FunctionType')

ArgType4 = TypeVar('ArgType4')

ArgType5 = TypeVar('ArgType5')

FuncSecond = TypeVar('FuncSecond')

ArgType7 = TypeVar('ArgType7')

ElseType = TypeVar('ElseType')

Func = TypeVar('Func')

ThenType = TypeVar('ThenType')

T = TypeVar('T')

TYP = TypeVar('TYP')

A = TypeVar('A')

ArgType1 = TypeVar('ArgType1')

class fast_multipole_embedder(object):

	class FMECollect(enum.Enum):

		NoFactor = enum.auto()

		EdgeFactor = enum.auto()

		RepulsiveFactor = enum.auto()

		EdgeFactorRep = enum.auto()

		Tree2GraphOrder = enum.auto()

		ZeroThreadArray = enum.auto()

	class FMEEdgeForce(enum.Enum):

		SubRep = enum.auto()

		DivDegree = enum.auto()

	CoordInt : Type = int

	false_condition : Type = const_condition[ False ]

	MortonNR : Type = int

	#: the corresponding typedefs
	true_condition : Type = const_condition[ True ]

	TIME_STEP_NORMAL : int = ...

	TIME_STEP_PREP : int = ...

	USE_NODE_MOVE_RAD : int = ...

	ZERO_GLOBAL_ARRAY : int = ...

	def align_16_next_ptr(self, t : T) -> T:
		...

	def align_16_prev_ptr(self, t : T) -> T:
		...

	def collect_force_function(self, pLocalContext : FMELocalContext) -> CollectForceFunctor[ FLAGS ]:
		...

	@overload
	def createFuncInvoker(self, func : FunctionType) -> FuncInvoker[ FunctionType ]:
		...

	@overload
	def createFuncInvoker(self, func : FunctionType, _arg1 : ArgType1) -> FuncInvoker[ FunctionType, ArgType1 ]:
		...

	@overload
	def createFuncInvoker(self, func : FunctionType, _arg1 : ArgType1, _arg2 : ArgType2) -> FuncInvoker[ FunctionType, ArgType1, ArgType2 ]:
		...

	@overload
	def createFuncInvoker(self, func : FunctionType, _arg1 : ArgType1, _arg2 : ArgType2, _arg3 : ArgType3) -> FuncInvoker[ FunctionType, ArgType1, ArgType2, ArgType3 ]:
		...

	@overload
	def createFuncInvoker(self, func : FunctionType, _arg1 : ArgType1, _arg2 : ArgType2, _arg3 : ArgType3, _arg4 : ArgType4) -> FuncInvoker[ FunctionType, ArgType1, ArgType2, ArgType3, ArgType4 ]:
		...

	@overload
	def createFuncInvoker(self, func : FunctionType, _arg1 : ArgType1, _arg2 : ArgType2, _arg3 : ArgType3, _arg4 : ArgType4, _arg5 : ArgType5) -> FuncInvoker[ FunctionType, ArgType1, ArgType2, ArgType3, ArgType4, ArgType5 ]:
		...

	@overload
	def createFuncInvoker(self, func : FunctionType, _arg1 : ArgType1, _arg2 : ArgType2, _arg3 : ArgType3, _arg4 : ArgType4, _arg5 : ArgType5, _arg6 : ArgType6) -> FuncInvoker[ FunctionType, ArgType1, ArgType2, ArgType3, ArgType4, ArgType5, ArgType6 ]:
		...

	@overload
	def createFuncInvoker(self, func : FunctionType, _arg1 : ArgType1, _arg2 : ArgType2, _arg3 : ArgType3, _arg4 : ArgType4, _arg5 : ArgType5, _arg6 : ArgType6, _arg7 : ArgType7) -> FuncInvoker[ FunctionType, ArgType1, ArgType2, ArgType3, ArgType4, ArgType5, ArgType6, ArgType7, ArgType8 ]:
		...

	@overload
	def createFuncInvoker(self, func : FunctionType, _arg1 : ArgType1, _arg2 : ArgType2, _arg3 : ArgType3, _arg4 : ArgType4, _arg5 : ArgType5, _arg6 : ArgType6, _arg7 : ArgType7, _arg8 : ArgType8) -> FuncInvoker[ FunctionType, ArgType1, ArgType2, ArgType3, ArgType4, ArgType5, ArgType6, ArgType7, ArgType8 ]:
		...

	def edge_force_function(self, pLocalContext : FMELocalContext) -> EdgeForceFunctor[ FLAGS ]:
		...

	@overload
	def eval_direct(self, x : float, y : float, s : float, fx : float, fy : float, n : size_t) -> None:
		"""kernel function to evaluate forces between n points with coords x, y directly. result is stored in fx, fy"""
		...

	@overload
	def eval_direct(self, x1 : float, y1 : float, s1 : float, fx1 : float, fy1 : float, n1 : size_t, x2 : float, y2 : float, s2 : float, fx2 : float, fy2 : float, n2 : size_t) -> None:
		"""kernel function to evaluate forces between two sets of points with coords x1, y1 (x2, y2) directly. result is stored in fx1, fy1 (fx2, fy2"""
		...

	@overload
	def eval_direct_fast(self, x : float, y : float, s : float, fx : float, fy : float, n : size_t) -> None:
		"""kernel function to evaluate forces between n points with coords x, y directly. result is stored in fx, fy"""
		...

	@overload
	def eval_direct_fast(self, x1 : float, y1 : float, s1 : float, fx1 : float, fy1 : float, n1 : size_t, x2 : float, y2 : float, s2 : float, fx2 : float, fy2 : float, n2 : size_t) -> None:
		"""kernel function to evaluate forces between two sets of points with coords x1, y1 (x2, y2) directly. result is stored in fx1, fy1 (fx2, fy2"""
		...

	def eval_edges(self, graph : ArrayGraph, begin : int, end : int, fx : float, fy : float) -> None:
		...

	def fast_multipole_l2p(self, localCoeffiecients : float, numCoeffiecients : int, centerX : float, centerY : float, x : float, y : float, q : float, fx : float, fy : float) -> None:
		"""kernel function to evalute a local expansion at point x,y result is added to fx, fy"""
		...

	def fast_multipole_p2m(self, mulitCoeffiecients : float, numCoeffiecients : int, centerX : float, centerY : float, x : float, y : float, q : float) -> None:
		...

	def for_loop_array_set(self, threadNr : int, numThreads : int, a : TYP, n : int, value : TYP) -> None:
		...

	def func_comp(self, first : FuncFirst, second : FuncSecond) -> composition_functor[ FuncFirst, FuncSecond ]:
		"""create a functor composition of two functors"""
		...

	def gridGraph(self, G : Graph, n : int, m : int) -> None:
		...

	def if_then(self, cond : CondType, thenFunc : ThenType) -> if_then_else_functor[ CondType, ThenType ]:
		"""creates an if then functor with a condition and a then functor"""
		...

	def if_then_else(self, cond : CondType, thenFunc : ThenType, elseFunc : ElseType) -> if_then_else_functor[ CondType, ThenType, ElseType ]:
		"""creates an if then else functor with a condition and a then and an else functor"""
		...

	def is_align_16(self, ptr : T) -> bool:
		...

	def l2l_function(self, pLocalContext : FMELocalContext) -> l2l_functor:
		"""creates Local-to-Local functor"""
		...

	def l2p_function(self, pLocalContext : FMELocalContext) -> l2p_functor:
		"""creates Local-to-Point functor"""
		...

	def LQPointComparer(self, a : LinearQuadtree.LQPoint, b : LinearQuadtree.LQPoint) -> bool:
		...

	def m2l_function(self, pLocalContext : FMELocalContext) -> m2l_functor:
		"""creates Multipole-to-Local functor"""
		...

	def m2m_function(self, pLocalContext : FMELocalContext) -> m2m_functor:
		"""creates Multipole-to-Multipole functor"""
		...

	def min_max_x_function(self, pLocalContext : FMELocalContext) -> min_max_functor[ float ]:
		"""creates a min max functor for the x coords of the node"""
		...

	def min_max_y_function(self, pLocalContext : FMELocalContext) -> min_max_functor[ float ]:
		"""creates a min max functor for the y coords of the node"""
		...

	def mortonNumber(self, ix : C_T, iy : C_T) -> MNR_T:
		"""common template for bit-interleaving to compute the morton number assumes sizeOf(MNR_T) = 2*sizeOf(C_T)"""
		...

	def mortonNumberInv(self, mnr : MNR_T, x : C_T, y : C_T) -> None:
		"""common template for extracting the coordinates from a morton number assumes sizeOf(MNR_T) = 2*sizeOf(C_T)"""
		...

	def mostSignificantBit(self, n : T) -> int:
		"""returns the index of the most signficant bit set. 0 = most signif, bitlength-1 = least signif"""
		...

	def move_nodes(self, x : float, y : float, begin : int, end : int, fx : float, fy : float, t : float) -> float:
		...

	def node_move_function(self, pLocalContext : FMELocalContext) -> NodeMoveFunctor[ FLAGS ]:
		...

	def not_condition(self, func : Func) -> not_condition_functor[ Func ]:
		"""creator of the negator"""
		...

	def OGDF_FME_Print_Config(self) -> None:
		...

	@overload
	def __and__(self, lhs : int, rhs : FMECollect) -> int:
		...

	@overload
	def __and__(self, lhs : int, rhs : FMEEdgeForce) -> int:
		...

	@overload
	def __or__(self, lhs : FMECollect, rhs : FMECollect) -> int:
		...

	@overload
	def __or__(self, lhs : int, rhs : FMECollect) -> int:
		...

	def p2m_function(self, pLocalContext : FMELocalContext) -> p2m_functor:
		"""creates a Point-to-Multipole functor"""
		...

	def p2p_function(self, pLocalContext : FMELocalContext) -> p2p_functor:
		"""creates Local-to-Point functor"""
		...

	def pair_call(self, f : F, a : A) -> pair_call_functor[ F, A ]:
		"""creates a pair call resulting in a call f(a, *)"""
		...

	def pair_vice_versa(self, f : Func) -> pair_vice_versa_functor[ Func ]:
		"""creates a functor for invoking a functor for a pair(u,v) and then (v,u)"""
		...

	def prevPowerOfTwo(self, n : int) -> int:
		"""returns the prev power of two"""
		...

	@overload
	def printProfiledTime(self, t : float, text : str) -> None:
		...

	@overload
	def printProfiledTime(self, t : float, sum : float, text : str) -> None:
		...

	def pushBackEdge(self, a : int, b : int, edgeInform : Callable, nodeInform : Callable, e_index : int) -> None:
		"""Helper method used byArrayGraphandWSPD."""
		...

	def randomGridGraph(self, G : Graph, n : int, m : int, missinNodesPercentage : float = 0.03) -> None:
		...

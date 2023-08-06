# file stubs/ogdf/fast_multipole_embedder/FMEMultipoleKernel.py generated from classogdf_1_1fast__multipole__embedder_1_1_f_m_e_multipole_kernel
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
F = TypeVar('F')

T = TypeVar('T')

C = TypeVar('C')

class FMEMultipoleKernel(ogdf.fast_multipole_embedder.FMEKernel):

	def __init__(self, pThread : FMEThread) -> None:
		...

	@overload
	def arrayPartition(self, n : int) -> ArrayPartition:
		"""creates an array partition with a default chunksize of 16"""
		...

	@overload
	def arrayPartition(self, n : int, threadNr : int, numThreads : int, chunkSize : int) -> ArrayPartition:
		"""returns an array partition for the given threadNr and thread count"""
		...

	def for_loop(self, partition : ArrayPartition, func : F) -> None:
		"""for loop on a partition"""
		...

	def for_tree_partition(self, functor : F) -> None:
		"""for loop on the tree partition"""
		...

	def multipoleApproxFinal(self, nodePointPartition : ArrayPartition) -> None:
		"""the final version, the wspd structure is only used for the top of the tree"""
		...

	def multipoleApproxNoWSPDStructure(self, nodePointPartition : ArrayPartition) -> None:
		"""new but slower method, parallel wspd computation without using the wspd structure"""
		...

	def multipoleApproxSingleThreaded(self, nodePointPartition : ArrayPartition) -> None:
		"""the single threaded version without fences"""
		...

	def multipoleApproxSingleWSPD(self, nodePointPartition : ArrayPartition) -> None:
		"""the original algorithm which runs theWSPDcompletely single threaded"""
		...

	def __call__(self, globalContext : FMEGlobalContext) -> None:
		"""main function of the kernel"""
		...

	def quadtreeConstruction(self, nodePointPartition : ArrayPartition) -> None:
		"""sub procedure for quadtree construction"""
		...

	@overload
	def sort_parallel(self, ptr : T, n : int, comparer : C) -> None:
		"""lazy parallel sorting for num_threads = power of two"""
		...

	@overload
	def sort_parallel(self, ptr : T, n : int, comparer : C, threadNrBegin : int, numThreads : int) -> None:
		"""lazy parallel sorting for num_threads = power of two"""
		...

	def sort_single(self, ptr : T, n : int, comparer : C) -> None:
		"""sorting single threaded"""
		...

	def allocateContext(self, pGraph : ArrayGraph, pOptions : FMEGlobalOptions, numThreads : int) -> FMEGlobalContext:
		"""allocate the global and local contexts used by an instance of this kernel"""
		...

	def deallocateContext(self, globalContext : FMEGlobalContext) -> None:
		"""free the global and local context"""
		...

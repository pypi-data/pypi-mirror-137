# file stubs/ogdf/fast_multipole_embedder/FMEThreadPool.py generated from classogdf_1_1fast__multipole__embedder_1_1_f_m_e_thread_pool
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
ArgType1 = TypeVar('ArgType1')

KernelType = TypeVar('KernelType')

class FMEThreadPool(object):

	def __init__(self, numThreads : int) -> None:
		...

	def __destruct__(self) -> None:
		...

	def numThreads(self) -> int:
		"""returns the number of threads in this pool"""
		...

	def runKernel(self, arg1 : ArgType1) -> None:
		...

	def runThreads(self) -> None:
		"""runs one iteration. This call blocks the main thread"""
		...

	def syncBarrier(self) -> Barrier:
		"""returns the barrier instance used to sync the threads during execution"""
		...

	def thread(self, threadNr : int) -> FMEThread:
		"""returns the threadNr-th thread"""
		...

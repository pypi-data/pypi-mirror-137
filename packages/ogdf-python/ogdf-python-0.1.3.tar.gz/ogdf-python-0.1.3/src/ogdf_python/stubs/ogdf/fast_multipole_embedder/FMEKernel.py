# file stubs/ogdf/fast_multipole_embedder/FMEKernel.py generated from classogdf_1_1fast__multipole__embedder_1_1_f_m_e_kernel
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class FMEKernel(object):

	def __init__(self, pThread : FMEThread) -> None:
		...

	def isMainThread(self) -> bool:
		"""returns true if this is the main thread ( the main thread is always the first thread )"""
		...

	def isSingleThreaded(self) -> bool:
		"""returns true if this run only uses one thread )"""
		...

	def numThreads(self) -> int:
		"""returns the total number of threads in the pool"""
		...

	def sync(self) -> None:
		...

	def threadNr(self) -> int:
		"""returns the index of the thread ( 0..numThreads()-1 )"""
		...

# file stubs/ogdf/fast_multipole_embedder/FMEThread.py generated from classogdf_1_1fast__multipole__embedder_1_1_f_m_e_thread
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class FMEThread(object):

	"""The fast multipole embedder work thread class."""

	def __init__(self, pThreadPool : FMEThreadPool, threadNr : int) -> None:
		"""construtor"""
		...

	def isMainThread(self) -> bool:
		"""returns true if this is the main thread ( the main thread is always the first thread )"""
		...

	def numThreads(self) -> int:
		"""returns the total number of threads in the pool"""
		...

	def __call__(self) -> None:
		"""the main work function"""
		...

	def setTask(self, pTask : FMETask) -> None:
		"""sets the actual task"""
		...

	def sync(self) -> None:
		"""thread sync call"""
		...

	def threadNr(self) -> int:
		"""returns the index of the thread ( 0..numThreads()-1 )"""
		...

	def threadPool(self) -> FMEThreadPool:
		"""returns the ThreadPool this thread belongs to"""
		...

	def unixSetAffinity(self) -> None:
		...

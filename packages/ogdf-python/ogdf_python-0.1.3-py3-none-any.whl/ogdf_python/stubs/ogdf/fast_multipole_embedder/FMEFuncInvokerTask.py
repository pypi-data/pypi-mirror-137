# file stubs/ogdf/fast_multipole_embedder/FMEFuncInvokerTask.py generated from classogdf_1_1fast__multipole__embedder_1_1_f_m_e_func_invoker_task
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
FuncInvokerType = TypeVar('FuncInvokerType')

class FMEFuncInvokerTask(ogdf.fast_multipole_embedder.FMETask, Generic[FuncInvokerType]):

	"""Class used to invoke a functor or function inside a thread."""

	def __init__(self, f : FuncInvokerType) -> None:
		"""constructor with an invoker"""
		...

	def doWork(self) -> None:
		"""overrides the taskdoWork()method and invokes the function or functor"""
		...

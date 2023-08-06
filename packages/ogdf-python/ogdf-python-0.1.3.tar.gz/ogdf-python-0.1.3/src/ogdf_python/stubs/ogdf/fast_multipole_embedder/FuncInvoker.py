# file stubs/ogdf/fast_multipole_embedder/FuncInvoker.py generated from structogdf_1_1fast__multipole__embedder_1_1_func_invoker_3_01_function_type_00_01_empty_arg_typec73d666f76a787bbc9f093b8017c64ea
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
FunctionType = TypeVar('FunctionType')

class FuncInvoker(Generic[FunctionType]):

	function : FunctionType = ...

	def __init__(self, f : FunctionType) -> None:
		...

	def __call__(self) -> None:
		...

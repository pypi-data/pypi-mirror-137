# file stubs/ogdf/dot/Ast/AList.py generated from structogdf_1_1dot_1_1_ast_1_1_a_list
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class AList(object):

	head : AsgnStmt = ...

	tail : AList = ...

	def __init__(self, headAsgnStmt : AsgnStmt, tailAList : AList) -> None:
		...

	def __destruct__(self) -> None:
		...

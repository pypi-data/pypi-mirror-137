# file stubs/ogdf/dot/Ast/StmtList.py generated from structogdf_1_1dot_1_1_ast_1_1_stmt_list
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class StmtList(object):

	head : Stmt = ...

	tail : StmtList = ...

	def __init__(self, headSTMT : Stmt, tailStatementList : StmtList) -> None:
		...

	def __destruct__(self) -> None:
		...

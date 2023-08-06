# file stubs/ogdf/dot/Ast/AttrList.py generated from structogdf_1_1dot_1_1_ast_1_1_attr_list
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class AttrList(object):

	head : AList = ...

	tail : AttrList = ...

	def __init__(self, headAList : AList, tailAttrList : AttrList) -> None:
		...

	def __destruct__(self) -> None:
		...

# file stubs/ogdf/BertaultLayout/CCElement.py generated from classogdf_1_1_bertault_layout_1_1_c_c_element
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class CCElement(object):

	"""Objects of this class are members of the containment heirarchy made in preprocessing stage of ImPrEd."""

	child : List[CCElement] = ...

	faceNum : int = ...

	num : int = ...

	parent : CCElement = ...

	root : bool = ...

	def init(self, i : int) -> None:
		...

# file stubs/ogdf/internal/GraphArrayIteratorBase.py generated from classogdf_1_1internal_1_1_graph_array_iterator_base
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
isConst = TypeVar('isConst')

ArrayType = TypeVar('ArrayType')

isArgConst = TypeVar('isArgConst')

# std::enable_if< isConst||!isArgConst, int >::type

class GraphArrayIteratorBase(Generic[ArrayType, isConst]):

	#: Type of the array.
	array_pointer_type : Type = Union[ArrayType, ArrayType]

	#: Index type of the associated array.
	key_type : Type = ArrayType.key_type

	#: Value type of the associated array.
	value_type : Type = Union[ArrayType.value_type, ArrayType.value_type]

	@overload
	def __init__(self) -> None:
		"""Constructor."""
		...

	@overload
	def __init__(self, iter : GraphArrayIteratorBase[ ArrayType, isArgConst ]) -> None:
		"""Constructor."""
		...

	@overload
	def __init__(self, iter : GraphArrayIteratorBase[ ArrayType, isConst ]) -> None:
		"""Copy constructor."""
		...

	@overload
	def __init__(self, key : key_type, a : array_pointer_type) -> None:
		"""Constructor."""
		...

	def key(self) -> key_type:
		"""Index inm_array."""
		...

	def __ne__(self, iter : GraphArrayIteratorBase[ ArrayType, isConst ]) -> bool:
		"""Inequality operator."""
		...

	def __deref__(self) -> value_type:
		"""Value ofm_arrayat indexm_key."""
		...

	def __preinc__(self) -> GraphArrayIteratorBase[ ArrayType, isConst ]:
		"""Increment operator (prefix)."""
		...

	def __postinc__(self, _ : int) -> GraphArrayIteratorBase[ ArrayType, isConst ]:
		"""Increment operator (postfix)."""
		...

	def __predec__(self) -> GraphArrayIteratorBase[ ArrayType, isConst ]:
		"""Decrement operator (prefix)."""
		...

	def __postdec__(self, _ : int) -> GraphArrayIteratorBase[ ArrayType, isConst ]:
		"""Decrement operator (postfix)."""
		...

	def __assign__(self, iter : GraphArrayIteratorBase[ ArrayType, isConst ]) -> GraphArrayIteratorBase[ ArrayType, isConst ]:
		"""Copy assignment operator."""
		...

	def __eq__(self, iter : GraphArrayIteratorBase[ ArrayType, isConst ]) -> bool:
		"""Equality operator."""
		...

	def value(self) -> value_type:
		"""Value ofm_arrayat indexm_key."""
		...

# file stubs/ogdf/MallocMemoryAllocator/__init__.py generated from classogdf_1_1_malloc_memory_allocator
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class MallocMemoryAllocator(object):

	"""Implements a simple memory manager usingmalloc()andfree()."""

	def __init__(self) -> None:
		...

	def __destruct__(self) -> None:
		...

	@overload
	def allocate(self, nBytes : size_t) -> None:
		"""Allocates memory of sizenBytes."""
		...

	@overload
	def allocate(self, nBytes : size_t, _ : str, _ : int) -> None:
		"""Allocates memory of sizenBytes."""
		...

	def checkSize(self, _ : size_t) -> bool:
		"""Always returns true since we simply trust malloc()."""
		...

	def cleanup(self) -> None:
		...

	def deallocate(self, _ : size_t, p : None) -> None:
		"""Deallocates memory at addressp. We do not keep track of the size of the deallocated object."""
		...

	def deallocateList(self, _ : size_t, pHead : None, pTail : None) -> None:
		"""Deallocate a complete list starting atpHeadand ending atpTail."""
		...

	@overload
	def flushPool(self) -> None:
		...

	@overload
	def flushPool(self, _ : int) -> None:
		...

	def memoryAllocatedInBlocks(self) -> size_t:
		"""Always returns 0, since no blocks are allocated."""
		...

	def memoryInFreelist(self) -> size_t:
		"""Always returns 0, since no blocks are allocated."""
		...

	def memoryInGlobalFreeList(self) -> size_t:
		"""Always returns 0, since no blocks are allocated."""
		...

	def memoryInThreadFreeList(self) -> size_t:
		"""Always returns 0, since no blocks are allocated."""
		...

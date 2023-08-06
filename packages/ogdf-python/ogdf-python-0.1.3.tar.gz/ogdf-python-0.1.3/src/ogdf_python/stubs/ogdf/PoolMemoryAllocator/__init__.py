# file stubs/ogdf/PoolMemoryAllocator/__init__.py generated from classogdf_1_1_pool_memory_allocator
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class PoolMemoryAllocator(object):

	"""Allocates memory in large chunks for better runtime."""

	def __init__(self) -> None:
		...

	def __destruct__(self) -> None:
		...

	def allocate(self, nBytes : size_t) -> None:
		"""Allocates memory of sizenBytes."""
		...

	def checkSize(self, nBytes : size_t) -> bool:
		"""Returns true iffallocatecan be invoked withnBytes."""
		...

	def cleanup(self) -> None:
		"""Frees all allocated memory."""
		...

	def deallocate(self, nBytes : size_t, p : None) -> None:
		"""Deallocates memory at addresspwhich is of sizenBytes."""
		...

	def deallocateList(self, nBytes : size_t, pHead : None, pTail : None) -> None:
		"""Deallocate a complete list starting atpHeadand ending atpTail."""
		...

	def defrag(self) -> None:
		"""Defragments the global free lists."""
		...

	def flushPool(self) -> None:
		"""Flushes all free but allocated bytes (s_tp) to the thread-global list (s_pool) of allocated bytes."""
		...

	def memoryAllocatedInBlocks(self) -> size_t:
		"""Returns the total amount of memory (in bytes) allocated from the system."""
		...

	def memoryInGlobalFreeList(self) -> size_t:
		"""Returns the total amount of memory (in bytes) available in the global free lists."""
		...

	def memoryInThreadFreeList(self) -> size_t:
		"""Returns the total amount of memory (in bytes) available in the thread's free lists."""
		...

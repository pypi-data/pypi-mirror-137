# file stubs/ogdf/System.py generated from classogdf_1_1_system
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class System(object):

	"""System specific functionality."""

	# Memory

	def alignedMemoryAlloc16(self, size : size_t) -> None:
		...

	def alignedMemoryFree(self, p : None) -> None:
		...

	def pageSize(self) -> int:
		"""Returns the page size of virtual memory (in bytes)."""
		...

	def physicalMemory(self) -> int:
		"""Returns the total size of physical memory (in bytes)."""
		...

	def availablePhysicalMemory(self) -> int:
		"""Returns the size of available (free) physical memory (in bytes)."""
		...

	def memoryUsedByProcess(self) -> size_t:
		"""Returns the amount of memory (in bytes) allocated by the process."""
		...

	def peakMemoryUsedByProcess(self) -> size_t:
		"""Returns the maximal amount of memory (in bytes) used by the process (Windows/Cygwin only)."""
		...

	def memoryAllocatedByMemoryManager(self) -> size_t:
		"""Returns the amount of memory (in bytes) allocated by OGDF's memory manager."""
		...

	def memoryInGlobalFreeListOfMemoryManager(self) -> size_t:
		"""Returns the amount of memory (in bytes) contained in the global free list of OGDF's memory manager."""
		...

	def memoryInThreadFreeListOfMemoryManager(self) -> size_t:
		"""Returns the amount of memory (in bytes) contained in the thread's free list of OGDF's memory manager."""
		...

	def memoryAllocatedByMalloc(self) -> size_t:
		"""Returns the amount of memory (in bytes) allocated on the heap (e.g., with malloc)."""
		...

	def memoryInFreelistOfMalloc(self) -> size_t:
		"""Returns the amount of memory (in bytes) contained in free chunks on the heap."""
		...

	# Measuring time

	def getHPCounter(self, counter : int) -> None:
		"""Returns the current value of the high-performance counter incounter."""
		...

	def elapsedSeconds(self, startCounter : int, endCounter : int) -> float:
		"""Returns the elapsed time (in seconds) betweenstartCounterandendCounter."""
		...

	def usedRealTime(self, t : int) -> int:
		"""Returns the elapsed time (in milliseconds) betweentand now."""
		...

	def realTime(self) -> int:
		"""Returns the current time point of the real time wall clock."""
		...

	# Process information

	def getProcessID(self) -> int:
		"""Returns the process ID of the current process."""
		...

	# Processor information

	def cpuFeatures(self) -> int:
		"""Returns the bit vector describing the CPU features supported on current system."""
		...

	def cpuSupports(self, feature : CPUFeature) -> bool:
		"""Returns true if the CPU supportsfeature."""
		...

	def cacheSizeKBytes(self) -> int:
		"""Returns the L2-cache size (in KBytes)."""
		...

	def cacheLineBytes(self) -> int:
		"""Returns the number of bytes in a cache line."""
		...

	def numberOfProcessors(self) -> int:
		"""Returns the number of processors (cores) available on the current system."""
		...

	def init(self) -> None:
		"""Static initilization routine (automatically called)."""
		...

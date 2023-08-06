# file stubs/ogdf/Configuration.py generated from classogdf_1_1_configuration
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Configuration(object):

	"""Provides information about how OGDF has been configured."""

	class LPSolver(enum.Enum):

		"""Specifies the LP-solver used by OGDF."""

		#: no LP-solver available
		_None = enum.auto()

		#: COIN-OR LP-solver (Clp)
		Clp = enum.auto()

		#: Symphony.
		Symphony = enum.auto()

		#: CPLEX (commercial)
		CPLEX = enum.auto()

		#: Gurobi (commercial)
		Gurobi = enum.auto()

		STOP = enum.auto()

	class MemoryManager(enum.Enum):

		"""Specifies the memory-manager used by OGDF."""

		#: thread-safe pool allocator
		PoolTS = enum.auto()

		#: non-thread-safe pool allocator
		PoolNTS = enum.auto()

		#: malloc/free allocator
		Malloc = enum.auto()

		STOP = enum.auto()

	class System(enum.Enum):

		"""Specifies the operating system for which OGDF has been configured/built."""

		#: not known (inproper configuration)
		Unknown = enum.auto()

		#: Windows.
		Windows = enum.auto()

		#: Unix/Linux.
		Unix = enum.auto()

		#: Apple OSX.
		OSX = enum.auto()

		STOP = enum.auto()

	def haveAbacus(self) -> bool:
		"""Returns whether OGDF has been configured with ABACUS support."""
		...

	def haveCoin(self) -> bool:
		"""Returns whether OGDF has been configured with COIN support."""
		...

	def haveLPSolver(self) -> bool:
		"""Returns whether OGDF has been configured with LP-solver support."""
		...

	@overload
	def toString(self, lps : LPSolver) -> str:
		"""Convertslpsto a (readable) string."""
		...

	@overload
	def toString(self, mm : MemoryManager) -> str:
		"""Convertsmmto a (readable) string."""
		...

	@overload
	def toString(self, sys : System) -> str:
		"""Convertssysto a (readable) string."""
		...

	def whichLPSolver(self) -> LPSolver:
		"""Returns the LP-solver used by OGDF."""
		...

	def whichMemoryManager(self) -> MemoryManager:
		"""Returns the memory manager used by OGDF."""
		...

	def whichSystem(self) -> System:
		"""Returns the operating system for which OGDF has been configured."""
		...

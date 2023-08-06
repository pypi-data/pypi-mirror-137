# file stubs/ogdf/Logger.py generated from classogdf_1_1_logger
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Logger(object):

	"""Centralized global and local logging facility working on streams likestd::cout."""

	# Usage

	def is_lout(self, level : Level = Level.Default) -> bool:
		"""returns true if such an lout command will result in text being printed"""
		...

	def lout(self, level : Level = Level.Default) -> std.ostream:
		"""stream for logging-output (local)"""
		...

	def sout(self) -> std.ostream:
		"""stream for statistic-output (local)"""
		...

	def fout(self) -> std.ostream:
		"""stream for forced output (local)"""
		...

	# Static usage

	def is_slout(self, level : Level = Level.Default) -> bool:
		"""returns true if such an slout command will result in text being printed"""
		...

	def slout(self, level : Level = Level.Default) -> std.ostream:
		"""stream for logging-output (global)"""
		...

	def ssout(self) -> std.ostream:
		"""stream for statistic-output (global)"""
		...

	def sfout(self) -> std.ostream:
		"""stream for forced output (global)"""
		...

	# Static internal library usage

	def is_ilout(self, level : Level = Level.Default) -> bool:
		"""stream for logging-output (global; used by internal libraries, e.g. Abacus) returns true if such an ilout command will result in text being printed"""
		...

	def ilout(self, level : Level = Level.Default) -> std.ostream:
		...

	def ifout(self) -> std.ostream:
		"""stream for forced output (global; used by internal libraries, e.g. Abacus)"""
		...

	# Local

	@overload
	def localLogLevel(self) -> Level:
		"""gives the local log-level"""
		...

	@overload
	def localLogLevel(self, level : Level) -> None:
		"""sets the local log-level"""
		...

	@overload
	def localLogMode(self) -> LogMode:
		"""gives the local log-mode"""
		...

	@overload
	def localLogMode(self, m : LogMode) -> None:
		"""sets the local log-mode"""
		...

	# Global

	@overload
	def globalLogLevel(self) -> Level:
		"""gives the global log-level"""
		...

	@overload
	def globalLogLevel(self, level : Level) -> None:
		"""sets the global log-level"""
		...

	@overload
	def globalInternalLibraryLogLevel(self) -> Level:
		"""gives the internal-library log-level"""
		...

	@overload
	def globalInternalLibraryLogLevel(self, level : Level) -> None:
		"""sets the internal-library log-level"""
		...

	@overload
	def globalMinimumLogLevel(self) -> Level:
		"""gives the globally minimally required log-level"""
		...

	@overload
	def globalMinimumLogLevel(self, level : Level) -> None:
		"""sets the globally minimally required log-level"""
		...

	@overload
	def globalStatisticMode(self) -> bool:
		"""returns true if we are globally in statistic mode"""
		...

	@overload
	def globalStatisticMode(self, s : bool) -> None:
		"""sets whether we are globally in statistic mode"""
		...

	def setWorldStream(self, o : std.ostream) -> None:
		"""change the stream to which allowed output is written (by default:std::cout)"""
		...

	# Effective

	def effectiveLogLevel(self) -> Level:
		"""obtain the effective log-level for the Logger-object (i.e., resolve the dependencies on the global settings)"""
		...

	def effectiveStatisticMode(self) -> bool:
		"""returns true if the Logger-object is effectively in statistic-mode (as this might be depending on the global settings)"""
		...

	class Level(enum.Enum):

		"""supported log-levels from lowest to highest importance"""

		Minor = enum.auto()

		Medium = enum.auto()

		Default = enum.auto()

		High = enum.auto()

		Alarm = enum.auto()

		Force = enum.auto()

	class LogMode(enum.Enum):

		"""Local log-modes."""

		#: the object is in the same mode as the static Logger-class (i.e., global settings)
		Global = enum.auto()

		#: the object is in logging mode, but uses the globalLogLevel
		GlobalLog = enum.auto()

		#: the object is in logging mode, using its own localLogLevel
		Log = enum.auto()

		#: the object is in statistic mode
		Statistic = enum.auto()

	@overload
	def __init__(self) -> None:
		"""creates a new Logger-object withLogMode::Globaland local log-level equal globalLogLevel"""
		...

	@overload
	def __init__(self, level : Level) -> None:
		"""creates a new Logger-object withLogMode::Globaland given local log-level"""
		...

	@overload
	def __init__(self, m : LogMode) -> None:
		"""creates a new Logger-object with given log-mode and local log-level equal globalLogLevel"""
		...

	@overload
	def __init__(self, m : LogMode, level : Level) -> None:
		"""creates a new Logger-object with given log-mode and given local log-level"""
		...

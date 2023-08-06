# file stubs/ogdf/CoinManager.py generated from classogdf_1_1_coin_manager
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class CoinManager(object):

	"""If you use COIN-OR, you should use this class."""

	#: The OGDFLoggerwhich will determine the log level for a new instance returned by createCorrectOsiSolverInterface.
	CoinLog : Logger = ...

	def createCorrectOsiSolverInterface(self) -> OsiSolverInterface:
		"""Get a new solver and set its initial log level according to the level of CoinLog."""
		...

	def updateLogging(self, osi : OsiSolverInterface) -> None:
		"""Update the log level of the CoinMessageHandler associated withosito match the log level of theogdf::LoggerCoinLog."""
		...

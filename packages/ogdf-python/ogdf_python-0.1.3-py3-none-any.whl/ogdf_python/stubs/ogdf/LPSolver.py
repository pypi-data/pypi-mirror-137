# file stubs/ogdf/LPSolver.py generated from classogdf_1_1_l_p_solver
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class LPSolver(object):

	class OptimizationGoal(enum.Enum):

		Minimize = enum.auto()

		Maximize = enum.auto()

	class Status(enum.Enum):

		Optimal = enum.auto()

		Infeasible = enum.auto()

		Unbounded = enum.auto()

	def __init__(self) -> None:
		...

	def __destruct__(self) -> None:
		...

	def checkFeasibility(self, matrixBegin : Array[  int ], matrixCount : Array[  int ], matrixIndex : Array[  int ], matrixValue : Array[ float ], rightHandSide : Array[ float ], equationSense : Array[  int ], lowerBound : Array[ float ], upperBound : Array[ float ], x : Array[ float ]) -> bool:
		...

	def infinity(self) -> float:
		...

	def optimize(self, goal : OptimizationGoal, obj : Array[ float ], matrixBegin : Array[  int ], matrixCount : Array[  int ], matrixIndex : Array[  int ], matrixValue : Array[ float ], rightHandSide : Array[ float ], equationSense : Array[  int ], lowerBound : Array[ float ], upperBound : Array[ float ], optimum : float, x : Array[ float ]) -> Status:
		...

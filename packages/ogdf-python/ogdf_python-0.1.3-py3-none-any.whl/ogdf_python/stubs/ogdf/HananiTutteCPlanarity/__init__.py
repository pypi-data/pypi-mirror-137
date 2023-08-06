# file stubs/ogdf/HananiTutteCPlanarity/__init__.py generated from classogdf_1_1_hanani_tutte_c_planarity
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class HananiTutteCPlanarity(object):

	"""C-planarity testing via Hanani-Tutte approach."""

	class Solver(enum.Enum):

		HananiTutte = enum.auto()

		HananiTutteVerify = enum.auto()

		ILP = enum.auto()

	class Status(enum.Enum):

		invalid = enum.auto()

		emptyAfterPreproc = enum.auto()

		cConnectedAfterPreproc = enum.auto()

		nonPlanarAfterPreproc = enum.auto()

		applyHananiTutte = enum.auto()

		applyILP = enum.auto()

		timeoutILP = enum.auto()

		errorILP = enum.auto()

	class SubType(enum.Enum):

		stVertex = enum.auto()

		stCluster = enum.auto()

		stEdge = enum.auto()

		stInnerCluster = enum.auto()

		stOuterCluster = enum.auto()

		stVertexCluster = enum.auto()

		stClusterCluster = enum.auto()

		stCrossCluster = enum.auto()

	class Type(enum.Enum):

		tVertex = enum.auto()

		tEdge = enum.auto()

	class Verification(enum.Enum):

		cPlanar = enum.auto()

		cPlanarVerified = enum.auto()

		nonCPlanarVerified = enum.auto()

		verificationFailed = enum.auto()

		timeout = enum.auto()

	def isCPlanar(self, C : ClusterGraph, doPreproc : bool = True, forceSolver : bool = False, solver : Solver = Solver.HananiTutte) -> Verification:
		...

	def numClustersPreproc(self) -> int:
		...

	def numEdgesPreproc(self) -> int:
		...

	def numMatrixCols(self) -> int:
		...

	def numMatrixRows(self) -> int:
		...

	def numNodesPreproc(self) -> int:
		...

	def preprocessing(self, C : ClusterGraph, G : Graph) -> None:
		...

	def status(self) -> Status:
		...

	def timeCreateSparse(self) -> int:
		...

	def timePrepare(self) -> int:
		...

	def timesolve(self) -> int:
		...

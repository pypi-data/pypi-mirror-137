# file stubs/ogdf/steiner_tree/goemans/BlowupGraph.py generated from classogdf_1_1steiner__tree_1_1goemans_1_1_blowup_graph
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

NODELIST = TypeVar('NODELIST')

class BlowupGraph(Generic[T]):

	"""A special-purpose blowup graph for gammoid computation: directed, with special source and target, with core edges (implemented as nodes)"""

	# Core edges and witness set management

	def addCore(self, e : node) -> None:
		"""Adds a core edge."""
		...

	def addWitness(self, e : node, f : edge) -> None:
		"""Addseto W(f)"""
		...

	def initCoreWitness(self) -> None:
		"""Finds a "random" set of core edges and "replace" found edges by nodes, also find the witness sets for the core edges."""
		...

	def makeCWCopy(self, edgeMap : HashArray[edge,edge]) -> None:
		"""Copies witness sets and core edges for a given copy map."""
		...

	def core(self) -> List[node]:
		"""Return list of core edges (implemented by nodes)"""
		...

	def delCore(self, e : node) -> None:
		"""Remove a core edge."""
		...

	def numberOfWitnesses(self, e : edge) -> int:
		"""Return the number of witnesses of an edge."""
		...

	def witnessList(self, e : node) -> ArrayBuffer[edge]:
		"""Return list of loss edges f in W(e)"""
		...

	# Getters for the blow-up graph (without core edges and witness sets)

	def getGraph(self) -> Graph:
		...

	def getSource(self) -> node:
		"""Returns the source node."""
		...

	def getPseudotarget(self) -> node:
		"""Returns the pseudotarget node."""
		...

	def getTarget(self) -> node:
		"""Returns the target node."""
		...

	def getCapacity(self, e : edge) -> int:
		"""Returns the capacity ofe."""
		...

	def capacities(self) -> EdgeArray[  int ]:
		"""Returns a reference to the edge array containing all capacities."""
		...

	def getCost(self, e : edge) -> T:
		"""Returns the cost ofe."""
		...

	def getOriginal(self, v : node) -> node:
		"""Returns the original node ofv."""
		...

	def getLCM(self) -> int:
		"""Returns the least common multiple of all denominators."""
		...

	def getY(self) -> int:
		"""Returns the y-value of all terminals."""
		...

	def terminals(self) -> List[node]:
		"""Returns a reference to the list containing all terminals in the blowup graph."""
		...

	def isTerminal(self, v : node) -> bool:
		"""Returns true if and only ifvis a terminal."""
		...

	# Getters for core edges

	def getCoreCapacity(self, v : node) -> T:
		"""Get capacity of a core edge."""
		...

	def getCoreCost(self, v : node) -> T:
		"""Get cost of a core edge."""
		...

	def computeCoreWeight(self, v : node) -> float:
		"""Compute the weight of a core edge."""
		...

	def computeLCM(self) -> None:
		"""Computes the least common multiple of the values assigned to the full components."""
		...

	def initBlowupGraphComponent(self, copy : NodeArray[node], start : adjEntry, cap : int) -> node:
		"""Does a bfs of the component tree to adddirectedcomponents with the first terminal as root."""
		...

	def initBlowupGraphComponents(self, originalGraph : EdgeWeightedGraph[ T ], terminals : List[node]) -> None:
		"""Initializes all components in the blowup graph as well as core edges and witness sets."""
		...

	def initNode(self, v : node) -> node:
		...

	def initPseudotarget(self) -> None:
		"""Connects pseudotarget."""
		...

	def initSource(self, roots : ArrayBuffer[ std.pair[node,  int ]]) -> None:
		"""Connects source to component roots."""
		...

	def initTarget(self) -> None:
		"""Connects target."""
		...

	def initTerminal(self, t : node) -> node:
		"""Inserts a terminal."""
		...

	def setCapacity(self, e : edge, capacity : int) -> None:
		...

	def updateSourceAndTargetArcCapacities(self, v : node) -> int:
		"""Updates arc capacities s->v and v->t."""
		...

	def __init__(self, G : EdgeWeightedGraph[ T ], terminals : List[node], fullCompStore : FullComponentWithExtraStore[ T, float ], ceModule : CoreEdgeModule[ T ], eps : float = 1e-8) -> None:
		"""Initializes a blowup graph including core edges and witness sets."""
		...

	@overload
	def contract(self, v : node, t : node) -> None:
		"""Contracts nodevand terminaltintov."""
		...

	@overload
	def contract(self, nodes : NODELIST) -> None:
		"""Contractsnodes."""
		...

	def copyComponent(self, origEdge : edge, origCap : int, copyCap : int) -> None:
		"""Copy a component in the blowup graph and set original capacity toorigCapand capacity of copy tocopyCap."""
		...

	def delEdges(self, edges : ArrayBuffer[edge]) -> None:
		"""Removes edges inedges."""
		...

	def findRootEdge(self, v : node) -> edge:
		"""Finds the root node of a component given byv, an arbitrary inner nonterminal of the component."""
		...

	def newEdge(self, v : node, w : node, cost : T, capacity : int) -> edge:
		"""Adds and returns a new edge betweenvandwof specifiedcostandcapacity."""
		...

	def removeBasis(self, v : node) -> None:
		"""Removes a basis and cleans up."""
		...

	def removeIsolatedTerminals(self) -> None:
		"""Removes isolated terminals."""
		...

	def updateSpecialCapacities(self) -> None:
		"""Updates capacities from source to terminals and terminals to pseudotarget."""
		...

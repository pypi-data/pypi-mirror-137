# file stubs/ogdf/steiner_tree/FullComponentStore/Metadata.py generated from structogdf_1_1steiner__tree_1_1_full_component_store_1_1_metadata_3_01_y_00_01typename_01std_1_1c1bea5a302d542e258ec84da66230b4c
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
Y = TypeVar('Y')

class Metadata(Generic[Y]):

	#: Cost.
	cost : T = ...

	extra : Y = ...

	#: Adjacency entry on a terminal where a non-terminal BFS yields the component.
	start : adjEntry = ...

	#: Terminals, sorted by node index.
	terminals : Array[node] = ...

	def __init__(self) -> None:
		...

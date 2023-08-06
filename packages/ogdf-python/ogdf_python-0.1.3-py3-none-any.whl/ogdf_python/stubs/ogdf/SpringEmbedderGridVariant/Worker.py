# file stubs/ogdf/SpringEmbedderGridVariant/Worker.py generated from classogdf_1_1_spring_embedder_grid_variant_1_1_worker
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Worker(ogdf.spring_embedder.WorkerBase[ Master, NodeInfo ]):

	def __init__(self, id : int, master : Master, vStartIndex : int, vStopIndex : int, vStart : node, vStop : node, eStartIndex : int) -> None:
		...

	def __call__(self) -> None:
		...

# file stubs/ogdf/LeftistOrdering/Candidate.py generated from structogdf_1_1_leftist_ordering_1_1_candidate
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Candidate(object):

	chain : List[adjEntry] = ...

	stopper : node = ...

	def __init__(self) -> None:
		...

# file stubs/ogdf/ExternE.py generated from structogdf_1_1_extern_e
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ExternE(object):

	"""List of externally active nodes strictly between x and y for minortypesBandE"""

	endnodes : SListPure[node] = ...

	externalPaths : SListPure[SListPure[edge] ] = ...

	startnodes : SListPure[  int ] = ...

	theNode : node = ...

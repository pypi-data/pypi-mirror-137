# file stubs/ogdf/OrderComparer.py generated from classogdf_1_1_order_comparer
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class OrderComparer(object):

	def __init__(self, _UPR : UpwardPlanRep, _H : Hierarchy) -> None:
		...

	def less(self, vH1 : node, vH2 : node) -> bool:
		"""Returns true iffvH1andvH2are placed on the same layer and nodevH1has to drawn on the left-hand side ofvH2(according tom_UPR)"""
		...

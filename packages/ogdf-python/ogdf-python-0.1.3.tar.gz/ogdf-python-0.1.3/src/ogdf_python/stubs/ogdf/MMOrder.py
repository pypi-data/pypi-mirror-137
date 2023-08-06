# file stubs/ogdf/MMOrder.py generated from classogdf_1_1_m_m_order
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class MMOrder(object):

	m_left : Array[node] = ...

	m_right : Array[node] = ...

	def __init__(self) -> None:
		...

	def init(self, PG : PlanRep, compOrder : ShellingOrderModule, adjExternal : adjEntry) -> None:
		...

	def len(self, k : int) -> int:
		...

	def length(self) -> int:
		...

	def __call__(self, k : int, i : int) -> node:
		...

	def __getitem__(self, k : int) -> ShellingOrderSet:
		...

	def rank(self, v : node) -> int:
		...

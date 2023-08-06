# file stubs/ogdf/gml/BasicHandler.py generated from classogdf_1_1gml_1_1_basic_handler
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class BasicHandler(ogdf.gml.IHandler):

	def __init__(self, GA : GraphAttributes = None) -> None:
		...

	def __destruct__(self) -> None:
		...

	def each(self, handler : Callable) -> BasicHandler:
		...

	def eachDouble(self, handler : Callable) -> BasicHandler:
		...

	def eachInt(self, handler : Callable) -> BasicHandler:
		...

	def eachString(self, handler : Callable) -> BasicHandler:
		...

	def handle(self, obj : Object) -> None:
		...

	def store(self, gattr : int, save : Callable) -> BasicHandler:
		...

	def storeDouble(self, gattr : int, save : Callable) -> BasicHandler:
		...

	def storeInt(self, gattr : int, save : Callable) -> BasicHandler:
		...

	def storeString(self, gattr : int, save : Callable) -> BasicHandler:
		...

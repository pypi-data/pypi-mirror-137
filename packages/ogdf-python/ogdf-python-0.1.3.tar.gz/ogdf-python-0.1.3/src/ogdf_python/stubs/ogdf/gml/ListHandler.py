# file stubs/ogdf/gml/ListHandler.py generated from classogdf_1_1gml_1_1_list_handler
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ListHandler(ogdf.gml.IHandler):

	def __init__(self, GA : GraphAttributes = None) -> None:
		...

	def __destruct__(self) -> None:
		...

	def afterEach(self, check : Callable) -> ListHandler:
		...

	def attribute(self, key : Key) -> BasicHandler:
		...

	def beforeEach(self, init : Callable) -> ListHandler:
		...

	def customAttribute(self, key : Key) -> CustomHandler:
		...

	def handle(self, obj : Object) -> None:
		...

	def listAttribute(self, key : Key) -> ListHandler:
		...

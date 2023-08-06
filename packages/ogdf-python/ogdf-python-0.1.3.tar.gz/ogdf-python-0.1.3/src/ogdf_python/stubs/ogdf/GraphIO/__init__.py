# file stubs/ogdf/GraphIO/__init__.py generated from classogdf_1_1_graph_i_o
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

# std::enable_if< std::is_floating_point< T >::value, bool >::type

# std::enable_if< std::is_integral< T >::value, bool >::type

class GraphIO(object):

	"""Utility class providing graph I/O in various exchange formats."""

	# Graphs

	@overload
	def read(self, G : Graph, filename : str, reader : ReaderFunc = None) -> bool:
		"""Reads graphGfrom a file with namefilenameand infers the used format from the file's extension."""
		...

	@overload
	def read(self, GA : GraphAttributes, G : Graph, filename : str, reader : AttrReaderFunc = None) -> bool:
		"""Reads graphGand its attributesGAfrom a file with namefilenameand infers the used format from the file's extension."""
		...

	@overload
	def read(self, CG : ClusterGraph, G : Graph, filename : str, reader : ClusterReaderFunc = None) -> bool:
		"""Reads graphGand a clusteringCGof G from a file with namefilenameand infers the used format from the file's extension."""
		...

	@overload
	def read(self, GA : ClusterGraphAttributes, CG : ClusterGraph, G : Graph, filename : str, reader : ClusterAttrReaderFunc = None) -> bool:
		"""Reads graphG, a clusteringCGof G and their attributesCGAfrom a file with namefilenameand infers the used format from the file's extension."""
		...

	@overload
	def read(self, G : Graph, _is : std.istream) -> bool:
		"""Reads graphGfrom a streamisand try to guess the contained format by trying all available readers."""
		...

	@overload
	def read(self, GA : GraphAttributes, G : Graph, _is : std.istream) -> bool:
		"""Reads graphGand its attributesGAfrom a streamisand try to guess the contained format by trying all available readers."""
		...

	@overload
	def read(self, CG : ClusterGraph, G : Graph, _is : std.istream) -> bool:
		"""Reads graphGand a clusteringCGof G from a streamisand try to guess the contained format by trying all available readers."""
		...

	@overload
	def read(self, GA : ClusterGraphAttributes, CG : ClusterGraph, G : Graph, _is : std.istream) -> bool:
		"""Reads graphG, a clusteringCGof G and their attributesGAfrom a streamisand try to guess the contained format by trying all available readers."""
		...

	@overload
	def write(self, G : Graph, filename : str, writer : WriterFunc = None) -> bool:
		"""Writes graphGto a file with namefilenameand infers the format to use from the file's extension."""
		...

	@overload
	def write(self, GA : GraphAttributes, filename : str, writer : AttrWriterFunc = None) -> bool:
		"""Writes graphGand its attributesGAto a file with namefilenameand infers the format to use from the file's extension."""
		...

	@overload
	def write(self, CG : ClusterGraph, filename : str, writer : ClusterWriterFunc = None) -> bool:
		"""Writes graphGand a clusteringCGof G to a file with namefilenameand infers the format to use from the file's extension."""
		...

	@overload
	def write(self, GA : ClusterGraphAttributes, filename : str, writer : ClusterAttrWriterFunc = None) -> bool:
		"""Writes graphG, a clusteringCGof G and their attributesCGAto a file with namefilenameand infers the format to use from the file's extension."""
		...

	# GML

	@overload
	def readGML(self, G : Graph, _is : std.istream) -> bool:
		"""Reads graphGin GML format from input streamis."""
		...

	@overload
	def writeGML(self, G : Graph, os : std.ostream) -> bool:
		"""Writes graphGin GML format to output streamos."""
		...

	@overload
	def readGML(self, C : ClusterGraph, G : Graph, _is : std.istream) -> bool:
		"""Reads clustered graph (C,G) in GML format from input streamis."""
		...

	@overload
	def writeGML(self, C : ClusterGraph, os : std.ostream) -> bool:
		"""Writes clustered graphCin GML format to output streamos."""
		...

	@overload
	def readGML(self, A : ClusterGraphAttributes, C : ClusterGraph, G : Graph, _is : std.istream) -> bool:
		"""Reads clustered graph (C,G) with attributesAin GML format from input streamis."""
		...

	@overload
	def writeGML(self, A : ClusterGraphAttributes, os : std.ostream) -> bool:
		"""Writes graph with attributesAin GML format to output streamos."""
		...

	@overload
	def readGML(self, A : GraphAttributes, G : Graph, _is : std.istream) -> bool:
		"""Reads graphGwith attributesAin GML format from input streamis."""
		...

	@overload
	def writeGML(self, A : GraphAttributes, os : std.ostream) -> bool:
		"""Writes graph with attributesAin GML format to output streamos."""
		...

	# Rome

	def readRome(self, G : Graph, _is : std.istream) -> bool:
		"""Reads graphGin Rome-Lib format from input streamis."""
		...

	def writeRome(self, G : Graph, os : std.ostream) -> bool:
		"""Writes graphGin Rome-Lib format to output streamos."""
		...

	# LEDA

	def readLEDA(self, G : Graph, _is : std.istream) -> bool:
		"""Reads graphGin LEDA graph format from input streamis."""
		...

	def writeLEDA(self, G : Graph, os : std.ostream) -> bool:
		"""Writes graphGin LEDA graph format to output streamos."""
		...

	# Chaco

	def readChaco(self, G : Graph, _is : std.istream) -> bool:
		"""Reads graphGin Chaco format from input streamis."""
		...

	def writeChaco(self, G : Graph, os : std.ostream) -> bool:
		"""Writes graphGin Chaco format to output streamos."""
		...

	# PMDissGraph

	def readPMDissGraph(self, G : Graph, _is : std.istream) -> bool:
		"""Reads graphGin a simple format as used in Petra Mutzel's thesis from input streamis."""
		...

	def writePMDissGraph(self, G : Graph, os : std.ostream) -> bool:
		"""Writes graphGin a simple format as used in Petra Mutzel's thesis to output streamos."""
		...

	# YGraph

	def readYGraph(self, G : Graph, _is : std.istream) -> bool:
		"""Reads graphGin Y-graph format from input streamis."""
		...

	# Graph6

	def readGraph6(self, G : Graph, _is : std.istream, forceHeader : bool = False) -> bool:
		"""Reads graphGin Graph6 format from input streamis."""
		...

	def writeGraph6(self, G : Graph, os : std.ostream) -> bool:
		"""Writes graphGin Graph6 format to output streamos."""
		...

	# Digraph6

	def readDigraph6(self, G : Graph, _is : std.istream, forceHeader : bool = False) -> bool:
		"""Reads graphGin Digraph6 format from input streamis."""
		...

	def writeDigraph6(self, G : Graph, os : std.ostream) -> bool:
		"""Writes graphGin Digraph6 format to output streamos."""
		...

	# Sparse6

	def readSparse6(self, G : Graph, _is : std.istream, forceHeader : bool = False) -> bool:
		"""Reads graphGin Sparse6 format from input streamis."""
		...

	def writeSparse6(self, G : Graph, os : std.ostream) -> bool:
		"""Writes graphGin Sparse6 format to output streamos."""
		...

	# MatrixMarket

	def readMatrixMarket(self, G : Graph, inStream : std.istream) -> bool:
		"""Reads graphGin Matrix Market exchange format from streaminStream."""
		...

	# Rudy

	@overload
	def readRudy(self, A : GraphAttributes, G : Graph, _is : std.istream) -> bool:
		"""Reads graphGwith edge weights stored inAin Rudy format from input streamis."""
		...

	@overload
	def readRudy(self, G : Graph, _is : std.istream) -> bool:
		"""Reads graphGin Rudy format from input streamis."""
		...

	def writeRudy(self, A : GraphAttributes, os : std.ostream) -> bool:
		"""Writes graph with edge weights stored inAin Rudy format to output streamos."""
		...

	# BENCH

	def readBENCH(self, G : Graph, hypernodes : List[node], shell : List[edge], _is : std.istream) -> bool:
		"""Reads a hypergraph (as point-based expansion) in BENCH format from input streamis."""
		...

	# PLA

	def readPLA(self, G : Graph, hypernodes : List[node], shell : List[edge], _is : std.istream) -> bool:
		"""Reads a hypergraph (as point-based expansion) in PLA format from input streamis."""
		...

	# GD-Challenge

	def readChallengeGraph(self, G : Graph, gl : GridLayout, _is : std.istream) -> bool:
		"""Reads graphGwith grid layoutglin GD-Challenge-format from input streamis."""
		...

	def writeChallengeGraph(self, G : Graph, gl : GridLayout, os : std.ostream) -> bool:
		"""Writes graphGwith grid layoutglin GD-Challenge-format to output streamos."""
		...

	# GraphML

	@overload
	def readGraphML(self, G : Graph, _is : std.istream) -> bool:
		"""Reads graphGin GraphML format from input streamis."""
		...

	@overload
	def readGraphML(self, C : ClusterGraph, G : Graph, _is : std.istream) -> bool:
		"""Reads clustered graph (C,G) in GraphML format from input streamis."""
		...

	@overload
	def readGraphML(self, A : GraphAttributes, G : Graph, _is : std.istream) -> bool:
		"""Reads graphGwith attributesAin GraphML format from input streamis."""
		...

	@overload
	def readGraphML(self, A : ClusterGraphAttributes, C : ClusterGraph, G : Graph, _is : std.istream) -> bool:
		"""Reads clustered graph (C,G) with attributesAin GraphML format from input streamis."""
		...

	@overload
	def writeGraphML(self, G : Graph, os : std.ostream) -> bool:
		"""Writes graphGin GraphML format to output streamos."""
		...

	@overload
	def writeGraphML(self, C : ClusterGraph, os : std.ostream) -> bool:
		"""Writes clustered graphCin GraphML format to output streamos."""
		...

	@overload
	def writeGraphML(self, A : GraphAttributes, os : std.ostream) -> bool:
		"""Writes graph with attributesAin GraphML format to output streamos."""
		...

	@overload
	def writeGraphML(self, A : ClusterGraphAttributes, os : std.ostream) -> bool:
		"""Writes graph with attributesAin GraphML format to output streamos."""
		...

	# DOT

	@overload
	def readDOT(self, G : Graph, _is : std.istream) -> bool:
		"""Reads graphGin DOT format from input streamis."""
		...

	@overload
	def readDOT(self, C : ClusterGraph, G : Graph, _is : std.istream) -> bool:
		"""Reads clustered graph (C,G) in DOT format from input streamis."""
		...

	@overload
	def readDOT(self, A : GraphAttributes, G : Graph, _is : std.istream) -> bool:
		"""Reads graphGwith attributesAin DOT format from input streamis."""
		...

	@overload
	def readDOT(self, A : ClusterGraphAttributes, C : ClusterGraph, G : Graph, _is : std.istream) -> bool:
		"""Reads clustered graph (C,G) with attributesAin DOT format from input streamis."""
		...

	@overload
	def writeDOT(self, G : Graph, os : std.ostream) -> bool:
		"""Writes graphGin DOT format to output streamos."""
		...

	@overload
	def writeDOT(self, C : ClusterGraph, os : std.ostream) -> bool:
		"""Writes clustered graphCin DOT format to output streamos."""
		...

	@overload
	def writeDOT(self, A : GraphAttributes, os : std.ostream) -> bool:
		"""Writes graph with attributesAin DOT format to output streamos."""
		...

	@overload
	def writeDOT(self, A : ClusterGraphAttributes, os : std.ostream) -> bool:
		"""Writes graph with attributesAin DOT format to output streamos."""
		...

	# GEXF

	@overload
	def readGEXF(self, G : Graph, _is : std.istream) -> bool:
		"""Reads graphGin GEXF format from input streamis."""
		...

	@overload
	def readGEXF(self, C : ClusterGraph, G : Graph, _is : std.istream) -> bool:
		"""Reads clustered graph (C,G) in GEXF format from input streamis."""
		...

	@overload
	def readGEXF(self, A : GraphAttributes, G : Graph, _is : std.istream) -> bool:
		"""Reads graphGwith attributesAin GEXF format from input streamis."""
		...

	@overload
	def readGEXF(self, A : ClusterGraphAttributes, C : ClusterGraph, G : Graph, _is : std.istream) -> bool:
		"""Reads clustered graph (C,G) with attributesAin GEXF format from input streamis."""
		...

	@overload
	def writeGEXF(self, G : Graph, os : std.ostream) -> bool:
		"""Writes graphGin GEXF format to output streamos."""
		...

	@overload
	def writeGEXF(self, C : ClusterGraph, os : std.ostream) -> bool:
		"""Writes clustered graphCin GEXF format to output streamos."""
		...

	@overload
	def writeGEXF(self, A : GraphAttributes, os : std.ostream) -> bool:
		"""Writes graph with attributesAin GEXF format to output streamos."""
		...

	@overload
	def writeGEXF(self, A : ClusterGraphAttributes, os : std.ostream) -> bool:
		"""Writes graph with attributesAin GEXF format to output streamos."""
		...

	# GDF

	@overload
	def readGDF(self, G : Graph, _is : std.istream) -> bool:
		"""Reads graphGin GDF format from input streamis."""
		...

	@overload
	def readGDF(self, A : GraphAttributes, G : Graph, _is : std.istream) -> bool:
		"""Reads graphGwith attributesAin GDF format from input streamis."""
		...

	@overload
	def writeGDF(self, G : Graph, os : std.ostream) -> bool:
		"""Writes graphGin GDF format to output streamos."""
		...

	@overload
	def writeGDF(self, A : GraphAttributes, os : std.ostream) -> bool:
		"""Writes graph with attributesAin GDF format to output streamos."""
		...

	# TLP

	@overload
	def readTLP(self, G : Graph, _is : std.istream) -> bool:
		"""Reads graphGin TLP format from input streamis."""
		...

	@overload
	def readTLP(self, C : ClusterGraph, G : Graph, _is : std.istream) -> bool:
		"""Reads clustered graph (C,G) in TLP format from input streamis."""
		...

	@overload
	def readTLP(self, A : GraphAttributes, G : Graph, _is : std.istream) -> bool:
		"""Reads graphGwith attributesAin TLP format from input streamis."""
		...

	@overload
	def readTLP(self, A : ClusterGraphAttributes, C : ClusterGraph, G : Graph, _is : std.istream) -> bool:
		"""Reads clustered graph (C,G) with attributesAin TLP format from input streamis."""
		...

	@overload
	def writeTLP(self, G : Graph, os : std.ostream) -> bool:
		"""Writes graphGin TLP format to output streamos."""
		...

	@overload
	def writeTLP(self, C : ClusterGraph, os : std.ostream) -> bool:
		"""Writes clustered graphCin TLP format to output streamos."""
		...

	@overload
	def writeTLP(self, A : GraphAttributes, os : std.ostream) -> bool:
		"""Writes graph with attributesAin TLP format to output streamos."""
		...

	@overload
	def writeTLP(self, A : ClusterGraphAttributes, os : std.ostream) -> bool:
		"""Writes graph with attributesAin TLP format to output streamos."""
		...

	# DL

	@overload
	def readDL(self, G : Graph, _is : std.istream) -> bool:
		"""Reads graphGin DL format from input streamis."""
		...

	@overload
	def readDL(self, A : GraphAttributes, G : Graph, _is : std.istream) -> bool:
		"""Reads graphGwith attributesAin DL format from input streamis."""
		...

	@overload
	def writeDL(self, G : Graph, os : std.ostream) -> bool:
		"""Writes graphGin DL format to output streamos."""
		...

	@overload
	def writeDL(self, A : GraphAttributes, os : std.ostream) -> bool:
		"""Writes graph with attributesAin DL format to output streamos."""
		...

	# STP

	@overload
	def readSTP(self, attr : GraphAttributes, G : Graph, terminals : List[node], isTerminal : NodeArray[ bool ], _is : std.istream) -> bool:
		"""Reads a graph in SteinLib format from std::istreamis."""
		...

	@overload
	def readSTP(self, attr : GraphAttributes, G : Graph, _is : std.istream) -> bool:
		"""Reads a graph in SteinLib format from std::istreamis."""
		...

	@overload
	def readSTP(self, G : Graph, _is : std.istream) -> bool:
		"""Reads a graph in SteinLib format from std::istreamis."""
		...

	@overload
	def readSTP(self, wG : EdgeWeightedGraph[ T ], terminals : List[node], isTerminal : NodeArray[ bool ], _is : std.istream) -> bool:
		"""Reads a SteinLib instance from an inputstreamisand converts it into a weighted graphwGand a set of terminal nodesterminals."""
		...

	@overload
	def writeSTP(self, attr : GraphAttributes, terminals : List[node], os : std.ostream, comments : str = "") -> bool:
		"""Writes an Steiner problem instance to an STP file."""
		...

	@overload
	def writeSTP(self, wG : EdgeWeightedGraph[ T ], terminals : List[node], os : std.ostream, comments : str = "") -> bool:
		"""Writes an Steiner problem instance to an STP file."""
		...

	# DMF

	@overload
	def readDMF(self, attr : GraphAttributes, graph : Graph, source : node, sink : node, _is : std.istream) -> bool:
		"""Reads a maximum flow instance in DIMACS format."""
		...

	@overload
	def readDMF(self, attr : GraphAttributes, graph : Graph, _is : std.istream) -> bool:
		"""Reads a maximum flow instance in DIMACS format."""
		...

	@overload
	def readDMF(self, graph : Graph, weights : EdgeArray[ T ], source : node, sink : node, _is : std.istream) -> bool:
		"""Reads a maximum flow instance in DIMACS format."""
		...

	@overload
	def readDMF(self, graph : Graph, _is : std.istream) -> bool:
		"""Reads a maximum flow instance in DIMACS format."""
		...

	@overload
	def writeDMF(self, attr : GraphAttributes, source : node, sink : node, os : std.ostream) -> bool:
		"""Writes a maximum flow problem instance to a DIMACS maximum flow file."""
		...

	@overload
	def writeDMF(self, graph : Graph, weights : EdgeArray[ T ], source : node, sink : node, os : std.ostream) -> bool:
		"""Writes a maximum flow problem instance to a DIMACS maximum flow file."""
		...

	# Graphs with subgraph

	def readEdgeListSubgraph(self, G : Graph, delEdges : List[edge], _is : std.istream) -> bool:
		"""Reads graphGwith subgraph defined bydelEdgesfrom streamis."""
		...

	def writeEdgeListSubgraph(self, G : Graph, delEdges : List[edge], os : std.ostream) -> bool:
		"""Writes graphGwith subgraph defined bydelEdgesto streamos."""
		...

	# Graphics formats

	@overload
	def drawSVG(self, A : GraphAttributes, os : std.ostream, settings : SVGSettings) -> bool:
		...

	@overload
	def drawSVG(self, A : GraphAttributes, os : std.ostream) -> bool:
		...

	@overload
	def drawSVG(self, A : GraphAttributes, filename : str, settings : SVGSettings = svgSettings) -> bool:
		...

	@overload
	def drawSVG(self, A : ClusterGraphAttributes, os : std.ostream, settings : SVGSettings) -> bool:
		...

	@overload
	def drawSVG(self, A : ClusterGraphAttributes, os : std.ostream) -> bool:
		...

	@overload
	def drawSVG(self, A : ClusterGraphAttributes, filename : str, settings : SVGSettings = svgSettings) -> bool:
		...

	# Utility functions for indentation

	def indentChar(self) -> int:
		"""Returns the currently used indentation character."""
		...

	def indentWidth(self) -> int:
		"""Returns the currently used indentation width."""
		...

	def setIndentChar(self, c : int) -> None:
		"""Sets the indentation character toc."""
		...

	def setIndentWidth(self, w : int) -> None:
		"""Sets the indentation width tow."""
		...

	def indent(self, os : std.ostream, depth : int) -> std.ostream:
		"""Prints indentation for indentationdepthto output streamosand returnsos."""
		...

	# Other utility functions

	svgSettings : SVGSettings = ...

	def setColorValue(self, value : int, setFunction : Callable) -> bool:
		"""Set a color value (R/G/B/A) based on an integer. Checks if the value is in the right range."""
		...

	@overload
	def getEdgeWeightFlag(self) -> int:
		"""ReturnsGraphAttributes::edgeIntWeight."""
		...

	@overload
	def getEdgeWeightFlag(self) -> int:
		"""ReturnsGraphAttributes::edgeDoubleWeight."""
		...

	@overload
	def getEdgeWeightAttribute(self, attr : GraphAttributes, e : edge) -> int:
		"""Returns a reference to the intWeight()-value ofattrfore."""
		...

	@overload
	def getEdgeWeightAttribute(self, attr : GraphAttributes, e : edge) -> float:
		"""Returns a reference to the doubleWeight()-value ofattrfore."""
		...

	#: Type of simple graph attributes reader functions working on streams.
	AttrReaderFunc : Type = bool()(GraphAttributes,Graph, std.istream )

	#: Type of simple graph attributes writer functions working on streams.
	AttrWriterFunc : Type = bool()(GraphAttributes, std.ostream )

	#: Type of cluster graph attributes reader functions working on streams.
	ClusterAttrReaderFunc : Type = bool()(ClusterGraphAttributes,ClusterGraph,Graph, std.istream )

	#: Type of cluster graph attributes writer functions working on streams.
	ClusterAttrWriterFunc : Type = bool()(ClusterGraphAttributes, std.ostream )

	#: Type of cluster graph reader functions working on streams.
	ClusterReaderFunc : Type = bool()(ClusterGraph,Graph, std.istream )

	#: Type of cluster graph writer functions working on streams.
	ClusterWriterFunc : Type = bool()(ClusterGraph, std.ostream )

	#: Type of simple graph reader functions working on streams.
	ReaderFunc : Type = bool()(Graph, std.istream )

	#: Type of simple graph writer functions working on streams.
	WriterFunc : Type = bool()(Graph, std.ostream )

	FILE_TYPE_MAP : Dict[ str,FileType] = ...

	FILE_TYPES : List[FileType] = ...

	logger : Logger = ...

	def getFileType(self, filename : str) -> FileType:
		...

	def getFileTypeMap(self) -> Dict[ str,FileType]:
		...

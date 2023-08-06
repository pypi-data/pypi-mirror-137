# file stubs/ogdf/BoyerMyrvold.py generated from classogdf_1_1_boyer_myrvold
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class BoyerMyrvold(ogdf.PlanarityModule):

	"""Wrapper class used for preprocessing and valid invocation of the planarity test."""

	#: The number of extracted Structures for statistical purposes.
	nOfStructures : int = ...

	#: ClassBoyerMyrvoldPlanaron heap.
	pBMP : BoyerMyrvoldPlanar = ...

	def clear(self) -> None:
		"""DeletesBoyerMyrvoldPlanaron heap."""
		...

	def __init__(self) -> None:
		"""Constructor."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...

	def isPlanar(self, g : Graph) -> bool:
		"""Returns true, iff a copy of the constant graphgis planar."""
		...

	def isPlanarDestructive(self, g : Graph) -> bool:
		"""Returns true, iffgis planar."""
		...

	def numberOfStructures(self) -> int:
		"""The number of extracted Structures for statistical purposes."""
		...

	@overload
	def planarEmbed(self, G : Graph) -> bool:
		"""Returns true, if G is planar, false otherwise. If true, G contains a planar embedding."""
		...

	@overload
	def planarEmbed(self, g : Graph, output : SList[KuratowskiWrapper], embeddingGrade : BoyerMyrvoldPlanar.EmbeddingGrade = BoyerMyrvoldPlanar.EmbeddingGrade.doNotFind, bundles : bool = False, limitStructures : bool = False, randomDFSTree : bool = False, avoidE2Minors : bool = True) -> bool:
		"""Returns an embedding, ifgis planar and Kuratowski Subdivisions otherwise."""
		...

	@overload
	def planarEmbed(self, g : Graph, output : SList[KuratowskiWrapper], embeddingGrade : int, bundles : bool = False, limitStructures : bool = False, randomDFSTree : bool = False, avoidE2Minors : bool = True) -> bool:
		"""Returns an embedding, ifgis planar and Kuratowski Subdivisions otherwise."""
		...

	@overload
	def planarEmbed(self, h : GraphCopySimple, output : SList[KuratowskiWrapper], embeddingGrade : BoyerMyrvoldPlanar.EmbeddingGrade = BoyerMyrvoldPlanar.EmbeddingGrade.doNotFind, bundles : bool = False, limitStructures : bool = False, randomDFSTree : bool = False, avoidE2Minors : bool = True) -> bool:
		"""Returns an embedding, if graph copyhis planar and Kuratowski Subdivisions otherwise."""
		...

	@overload
	def planarEmbed(self, h : GraphCopySimple, output : SList[KuratowskiWrapper], embeddingGrade : int, bundles : bool = False, limitStructures : bool = False, randomDFSTree : bool = False, avoidE2Minors : bool = True) -> bool:
		"""Returns an embedding, if graph copyhis planar and Kuratowski Subdivisions otherwise."""
		...

	@overload
	def planarEmbedDestructive(self, g : Graph, output : SList[KuratowskiWrapper], embeddingGrade : BoyerMyrvoldPlanar.EmbeddingGrade = BoyerMyrvoldPlanar.EmbeddingGrade.doNotFind, bundles : bool = False, limitStructures : bool = False, randomDFSTree : bool = False, avoidE2Minors : bool = True) -> bool:
		"""Returns an embedding, ifgis planar and Kuratowski Subdivisions otherwise."""
		...

	@overload
	def planarEmbedDestructive(self, g : Graph, output : SList[KuratowskiWrapper], embeddingGrade : int, bundles : bool = False, limitStructures : bool = False, randomDFSTree : bool = False, avoidE2Minors : bool = True) -> bool:
		"""Returns an embedding, ifgis planar and Kuratowski Subdivisions otherwise."""
		...

	def planarEmbedPlanarGraph(self, G : Graph) -> bool:
		"""Constructs a planar embedding of G.Ghasto be planar!"""
		...

	@overload
	def transform(self, source : KuratowskiWrapper, target : KuratowskiSubdivision, count : NodeArray[  int ], countEdge : EdgeArray[  int ]) -> None:
		"""TransformsKuratowskiWrapperinKuratowskiSubdivision."""
		...

	@overload
	def transform(self, sourceList : SList[KuratowskiWrapper], targetList : SList[KuratowskiSubdivision], g : Graph, onlyDifferent : bool = False) -> None:
		"""Transforms KuratowskiWrapper-List in KuratowskiSubdivision-List with respect to sieving constraints."""
		...

	@overload
	def transform(self, sourceList : SList[KuratowskiWrapper], targetList : SList[KuratowskiSubdivision], h : GraphCopySimple, onlyDifferent : bool = False) -> None:
		"""Transforms KuratowskiWrapper-List in KuratowskiSubdivision-List with respect to sieving constraints."""
		...

# file stubs/ogdf/GenericPoint.py generated from classogdf_1_1_generic_point
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class GenericPoint(Generic[T]):

	"""Parameterized base class for points."""

	#: The type for coordinates of the point.
	numberType : Type = T

	#: The x-coordinate.
	m_x : T = ...

	#: The y-coordinate.
	m_y : T = ...

	@overload
	def __init__(self, p : GenericPoint[ T ]) -> None:
		"""Copy constructor."""
		...

	@overload
	def __init__(self, x : T = 0, y : T = 0) -> None:
		"""Creates a generic point (x,y)."""
		...

	def angle(self, q : GenericPoint[ T ], r : GenericPoint[ T ]) -> float:
		"""Compute angle (in radians) between vectors."""
		...

	def angleDegrees(self, q : GenericPoint[ T ], r : GenericPoint[ T ]) -> float:
		"""Compute angle (in degrees) between vectors."""
		...

	def determinant(self, dv : GenericPoint[ T ]) -> T:
		"""Returns the determinant of the matrix (this,dv)."""
		...

	def distance(self, p : GenericPoint[ T ]) -> float:
		"""Returns the Euclidean distance betweenpand this point."""
		...

	def norm(self) -> float:
		"""Returns the norm of the point."""
		...

	def __ne__(self, p : GenericPoint[ T ]) -> bool:
		"""Inequality operator."""
		...

	def __mul__(self, dv : GenericPoint[ T ]) -> T:
		"""Returns the scalar product of this anddv."""
		...

	def __imul__(self, c : T) -> GenericPoint[ T ]:
		"""Point-wise multiplies this withc."""
		...

	def __add__(self, p : GenericPoint[ T ]) -> GenericPoint[ T ]:
		"""Addition of points."""
		...

	def __iadd__(self, p : GenericPoint[ T ]) -> GenericPoint[ T ]:
		"""Addspto this."""
		...

	def __sub__(self, p : GenericPoint[ T ]) -> GenericPoint[ T ]:
		"""Subtraction of points."""
		...

	def __isub__(self, p : GenericPoint[ T ]) -> GenericPoint[ T ]:
		"""Subtractspfrom this."""
		...

	def __idiv__(self, c : T) -> GenericPoint[ T ]:
		"""Point-wise divide this byc."""
		...

	def __lt__(self, p : GenericPoint[ T ]) -> bool:
		"""Operator 'less'. Returnstrueiff thexcoordinate of this is less than thexcoordinate ofpor, if they are equal, the same check is done for theycoordinate."""
		...

	def __assign__(self, p : GenericPoint[ T ]) -> GenericPoint[ T ]:
		"""Assignment operator."""
		...

	def __eq__(self, dp : GenericPoint[ T ]) -> bool:
		"""Equality operator."""
		...

	def __gt__(self, p : GenericPoint[ T ]) -> bool:
		"""Operator 'greater'. Returnstrueiffpis less than this."""
		...

	def orthogonal(self) -> GenericPoint[ T ]:
		"""Returns a vector that is orthogonal to this vector."""
		...

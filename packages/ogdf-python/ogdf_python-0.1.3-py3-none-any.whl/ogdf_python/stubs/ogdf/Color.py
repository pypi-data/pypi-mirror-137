# file stubs/ogdf/Color.py generated from classogdf_1_1_color
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Color(object):

	"""Colors represented as RGBA values."""

	class Name(enum.Enum):

		"""Named colors (same as SVG color keywords)."""

		Aliceblue = enum.auto()

		Antiquewhite = enum.auto()

		Aqua = enum.auto()

		Aquamarine = enum.auto()

		Azure = enum.auto()

		Beige = enum.auto()

		Bisque = enum.auto()

		Black = enum.auto()

		Blanchedalmond = enum.auto()

		Blue = enum.auto()

		Blueviolet = enum.auto()

		Brown = enum.auto()

		Burlywood = enum.auto()

		Cadetblue = enum.auto()

		Chartreuse = enum.auto()

		Chocolate = enum.auto()

		Coral = enum.auto()

		Cornflowerblue = enum.auto()

		Cornsilk = enum.auto()

		Crimson = enum.auto()

		Cyan = enum.auto()

		Darkblue = enum.auto()

		Darkcyan = enum.auto()

		Darkgoldenrod = enum.auto()

		Darkgray = enum.auto()

		Darkgreen = enum.auto()

		Darkgrey = enum.auto()

		Darkkhaki = enum.auto()

		Darkmagenta = enum.auto()

		Darkolivegreen = enum.auto()

		Darkorange = enum.auto()

		Darkorchid = enum.auto()

		Darkred = enum.auto()

		Darksalmon = enum.auto()

		Darkseagreen = enum.auto()

		Darkslateblue = enum.auto()

		Darkslategray = enum.auto()

		Darkslategrey = enum.auto()

		Darkturquoise = enum.auto()

		Darkviolet = enum.auto()

		Deeppink = enum.auto()

		Deepskyblue = enum.auto()

		Dimgray = enum.auto()

		Dimgrey = enum.auto()

		Dodgerblue = enum.auto()

		Firebrick = enum.auto()

		Floralwhite = enum.auto()

		Forestgreen = enum.auto()

		Fuchsia = enum.auto()

		Gainsboro = enum.auto()

		Ghostwhite = enum.auto()

		Gold = enum.auto()

		Goldenrod = enum.auto()

		Gray = enum.auto()

		Green = enum.auto()

		Greenyellow = enum.auto()

		Grey = enum.auto()

		Honeydew = enum.auto()

		Hotpink = enum.auto()

		Indianred = enum.auto()

		Indigo = enum.auto()

		Ivory = enum.auto()

		Khaki = enum.auto()

		Lavender = enum.auto()

		Lavenderblush = enum.auto()

		Lawngreen = enum.auto()

		Lemonchiffon = enum.auto()

		Lightblue = enum.auto()

		Lightcoral = enum.auto()

		Lightcyan = enum.auto()

		Lightgoldenrodyellow = enum.auto()

		Lightgray = enum.auto()

		Lightgreen = enum.auto()

		Lightgrey = enum.auto()

		Lightpink = enum.auto()

		Lightsalmon = enum.auto()

		Lightseagreen = enum.auto()

		Lightskyblue = enum.auto()

		Lightslategray = enum.auto()

		Lightslategrey = enum.auto()

		Lightsteelblue = enum.auto()

		Lightyellow = enum.auto()

		Lime = enum.auto()

		Limegreen = enum.auto()

		Linen = enum.auto()

		Magenta = enum.auto()

		Maroon = enum.auto()

		Mediumaquamarine = enum.auto()

		Mediumblue = enum.auto()

		Mediumorchid = enum.auto()

		Mediumpurple = enum.auto()

		Mediumseagreen = enum.auto()

		Mediumslateblue = enum.auto()

		Mediumspringgreen = enum.auto()

		Mediumturquoise = enum.auto()

		Mediumvioletred = enum.auto()

		Midnightblue = enum.auto()

		Mintcream = enum.auto()

		Mistyrose = enum.auto()

		Moccasin = enum.auto()

		Navajowhite = enum.auto()

		Navy = enum.auto()

		Oldlace = enum.auto()

		Olive = enum.auto()

		Olivedrab = enum.auto()

		Orange = enum.auto()

		Orangered = enum.auto()

		Orchid = enum.auto()

		Palegoldenrod = enum.auto()

		Palegreen = enum.auto()

		Paleturquoise = enum.auto()

		Palevioletred = enum.auto()

		Papayawhip = enum.auto()

		Peachpuff = enum.auto()

		Peru = enum.auto()

		Pink = enum.auto()

		Plum = enum.auto()

		Powderblue = enum.auto()

		Purple = enum.auto()

		Red = enum.auto()

		Rosybrown = enum.auto()

		Royalblue = enum.auto()

		Saddlebrown = enum.auto()

		Salmon = enum.auto()

		Sandybrown = enum.auto()

		Seagreen = enum.auto()

		Seashell = enum.auto()

		Sienna = enum.auto()

		Silver = enum.auto()

		Skyblue = enum.auto()

		Slateblue = enum.auto()

		Slategray = enum.auto()

		Slategrey = enum.auto()

		Snow = enum.auto()

		Springgreen = enum.auto()

		Steelblue = enum.auto()

		Tan = enum.auto()

		Teal = enum.auto()

		Thistle = enum.auto()

		Tomato = enum.auto()

		Turquoise = enum.auto()

		Violet = enum.auto()

		Wheat = enum.auto()

		White = enum.auto()

		Whitesmoke = enum.auto()

		Yellow = enum.auto()

		Yellowgreen = enum.auto()

	@overload
	def __init__(self) -> None:
		"""Creates an opaque black color."""
		...

	@overload
	def __init__(self, name : Color.Name) -> None:
		"""Creates a color from given color namename."""
		...

	@overload
	def __init__(self, str : str) -> None:
		"""Crates a color from stringstr."""
		...

	@overload
	def __init__(self, str : str) -> None:
		"""Crates a color from stringstr."""
		...

	@overload
	def __init__(self, r : int, g : int, b : int, a : int = 255) -> None:
		"""Creates a color from given RGBA-values."""
		...

	@overload
	def __init__(self, r : int, g : int, b : int, a : int = 255) -> None:
		"""Creates a color from given RGBA-values."""
		...

	@overload
	def alpha(self) -> int:
		"""Returns the alpha channel."""
		...

	@overload
	def alpha(self, a : int) -> None:
		"""Sets the alpha channel toa."""
		...

	@overload
	def blue(self) -> int:
		"""Returns the blue component."""
		...

	@overload
	def blue(self, b : int) -> None:
		"""Sets the blue component tob."""
		...

	def fromString(self, str : str) -> bool:
		"""Sets the color the the color defined bystr."""
		...

	@overload
	def green(self) -> int:
		"""Returns the green component."""
		...

	@overload
	def green(self, g : int) -> None:
		"""Sets the green component tog."""
		...

	def __ne__(self, c : Color) -> bool:
		"""Returns true iffcand this color differ in any component."""
		...

	def __eq__(self, c : Color) -> bool:
		"""Returns true iffcand this color are equal in every component."""
		...

	@overload
	def red(self) -> int:
		"""Returns the red component."""
		...

	@overload
	def red(self, r : int) -> None:
		"""Sets the red component tor."""
		...

	def toString(self) -> str:
		"""Converts the color to a string and returns it."""
		...

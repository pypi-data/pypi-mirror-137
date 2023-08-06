# file stubs/ogdf/Math/__init__.py generated from namespaceogdf_1_1_math
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
INDEX = TypeVar('INDEX')

T = TypeVar('T')

Is = TypeVar('Is')

Container = TypeVar('Container')

Args = TypeVar('Args')

class Math(object):

	compiletimeLimit = ...

	#: The Euler-Mascheroni constant gamma.
	gamma : float = ...

	#: The constant log(4.0).
	log_of_4 : float = ...

	#: The constant$\frac{180}{\pi}$.
	one_rad : float = ...

	#: The constant$\pi$.
	pi : float = ...

	#: The constant$\frac{\pi}{180}$.
	pi_180 : float = ...

	#: The constant$\frac{\pi}{2}$.
	pi_2 : float = ...

	def binomial(self, n : int, k : int) -> int:
		"""Returns$n \choose k$."""
		...

	def binomial_d(self, n : int, k : int) -> float:
		"""Returns$n \choose k$."""
		...

	def compiletimeHarmonic(self, n) -> float:
		...

	def degreesToRadians(self, angleInDegrees : float) -> float:
		"""Converts an angle from degrees to radians."""
		...

	def factorial(self, n : int) -> int:
		"""Returnsn!."""
		...

	def factorial_d(self, n : int) -> float:
		"""Returnsn!."""
		...

	def floorLog2(self, v : int) -> int:
		"""A method to obtain the rounded down binary logarithm ofv."""
		...

	@overload
	def gcd(self, numbers : Array[ T, INDEX ]) -> T:
		"""Returns the greatest common divisor of a list of numbers."""
		...

	@overload
	def gcd(self, a : T, b : T) -> T:
		"""Returns the greatest common divisor of two numbers."""
		...

	def generateCompiletimeHarmonics(self, _ : seq[ Is ]) -> compiletimeTable:
		...

	def getFraction(self, d : float, num : int, denom : int, epsilon : float = 5e-10, count : int = 10) -> None:
		"""Converts a double to a fraction."""
		...

	def harmonic(self, n) -> float:
		"""Returns then-thharmonic number or 1.0 ifn< 1."""
		...

	def lcm(self, a : T, b : T) -> T:
		"""Returns the least common multipler of two numbers."""
		...

	def log2(self, x : T) -> T:
		"""Returns the logarithm ofxto the base 2."""
		...

	def log4(self, x : float) -> float:
		"""Returns the logarithm ofxto the base 4."""
		...

	def maxValue(self, values : Container) -> Container.value_type:
		"""Returns the maximum of an iterable container of givenvalues."""
		...

	def mean(self, values : Container) -> float:
		"""Returns the mean of an iterable container of givenvalues."""
		...

	def minValue(self, values : Container) -> Container.value_type:
		"""Returns the minimum of an iterable container of givenvalues."""
		...

	@overload
	def nextPower2(self, arg1 : T, arg2 : T, args : Args) -> T:
		"""Returns the smallest power of 2 that is no less than the given (integral) arguments."""
		...

	@overload
	def nextPower2(self, x : T) -> T:
		"""Returns the smallest power of 2 that is no less than the given (integral) argument."""
		...

	def radiansToDegrees(self, angleInRadians : float) -> float:
		"""Converts an angle from radians to degrees."""
		...

	def sgn(self, val : T) -> int:
		"""Returns +1 for val > 0, 0 for val = 0, and -1 for val < 0."""
		...

	@overload
	def standardDeviation(self, values : Container) -> float:
		"""Returns the standard deviation of an iterable container of givenvalues."""
		...

	@overload
	def standardDeviation(self, values : Container, mean : float) -> float:
		"""Returns the standard deviation of an iterable container of givenvalues."""
		...

	def sum(self, values : Container) -> Container.value_type:
		"""Returns the sum of an iterable container of givenvalues."""
		...

	def updateMax(self, max : T, newValue : T) -> None:
		"""Stores the maximum ofmaxandnewValueinmax."""
		...

	def updateMin(self, min : T, newValue : T) -> None:
		"""Stores the minimum ofminandnewValueinmin."""
		...

"""Metrology APIs."""

from typing import Final, Protocol, Self, override, runtime_checkable

import optype as op

__version__: Final = "0.0.1.dev0"
__all__ = ["__version__", "Dimension", "Quantity", "Unit"]


@runtime_checkable
class Dimension(Protocol):
    def __mul__(self, other: Self, /) -> Self: ...
    def __truediv__(self, other: Self, /) -> Self: ...
    def __pow__(self, other: int, /) -> Self: ...

    def __rmul__(self, other: Self, /) -> Self: ...
    def __rtruediv__(self, other: Self, /) -> Self: ...

    def decompose(self, dimension_system: "DimensionSystem", /) -> "dict[Dimension, float | int]":
        """Decompose the dimension into its base dimensions and exponents.

        Parameters
        ----------
        dimension_system
            The dimension system to use for decomposition. This defines the base
            dimensions.

        Notes
        -----
        By far the most common dimension system is (Length, Mass, Time, Electric
        Current, Temperature, Amount of Substance, Luminous Intensity).
        Implementing libraries are free to make this the default dimension
        system and to set it as the default value in their ``decompose`` method.

        Examples
        --------
        As this is an API protocol, no runtime examples are possible. The
        following is an illustrative example:

        >>> import metrology as u

        >>> dim = u.Length / u.Time

        >>> dim_sys = u.DimensionSystem(u.Length, u.Time)
        >>> dim.decompose(dim_sys)
        {Length: 1, Time: -1}

        >>> dim_sys = u.DimensionSystem(u.Velocity)
        >>> dim.decompose(dim_sys)
        {Velocity: 1}

        """


@runtime_checkable
class DimensionSystem(Protocol):
    """A system of dimensions.

    This is a collection of base dimensions that can be used to decompose other
    dimensions. Most unit systems, like the International System of Units, are
    based on a dimension system of involving Length, Mass, Time, Electric
    Current, Temperature Amount of Substance, Luminous Intensity. However, other
    dimension systems are possible, such as 'natural' systems where the speed of
    light is set to 1. The `DimensionsSystem` class is the API for any choice of
    dimension system.

    Examples
    --------
    As this is an API protocol, no runtime examples are possible. The
    following is an illustrative example:

    >>> import metrology as u

    >>> dim_sys = u.DimensionSystem(u.Length, u.Time)

    >>> dim_sys = u.DimensionSystem(u.Velocity)

    """

    base_dimensions: tuple[Dimension, ...]
    """The base dimensions of the system."""


@runtime_checkable
class Unit(Protocol):
    @property
    def dimension(self) -> Dimension: ...

    def __mul__(self, other: Self, /) -> Self: ...
    def __truediv__(self, other: Self, /) -> Self: ...
    def __pow__(self, other: int | float, /) -> Self: ...

    def __rmul__(self, other: Self, /) -> Self: ...
    def __rtruediv__(self, other: Self, /) -> Self: ...

@runtime_checkable
class Quantity[V, U: Unit](Protocol):
    @property
    def value(self) -> V: ...
    @property
    def unit(self) -> U: ...

    ### Dunder Methods

    @override
    def __eq__[B](self: "Quantity[V, U]", other: "Quantity[op.CanEq[V, B], U]", /) -> B: ...  # type: ignore[override]  # pyright: ignore[reportIncompatibleMethodOverride]

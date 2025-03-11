"""Metrology APIs."""

from typing import Final, Protocol, Self, runtime_checkable

import optype as op

__version__: Final = "0.0.1.dev0"
__all__ = ["__version__", "Dimension", "Quantity", "Unit"]


@runtime_checkable
class Dimension(Protocol):
    def __mul__(self, other: Self, /) -> Self: ...
    def __truediv__(self, other: Self, /) -> Self: ...
    def __pow__(self, other: int, /) -> Self: ...


@runtime_checkable
class Unit(Protocol):
    @property
    def dimension(self) -> Dimension: ...

    def __mul__(self, other: Self, /) -> Self: ...
    def __truediv__(self, other: Self, /) -> Self: ...
    def __pow__(self, other: int | Self, /) -> Self: ...

    # debatable whether this should be standardised
    def __rlshift__[V](self, other: V) -> "Quantity[V, Self]": ...


@runtime_checkable
class Quantity[V, U: Unit](Protocol):
    @property
    def value(self) -> V: ...
    @property
    def unit(self) -> U: ...

    ### Dunder Methods

    def __eq__[B](self: "Quantity[V, U]", other: "Quantity[op.CanEq[V, B], U]", /) -> B: ...

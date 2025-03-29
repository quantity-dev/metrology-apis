"""Metrology APIs."""

from typing import TYPE_CHECKING, Final, Protocol, Self, override, runtime_checkable

import optype as op

if TYPE_CHECKING:
    import fractions


__version__: Final = "0.0.1.dev0"
__all__ = ["__version__", "Dimension", "Quantity", "Unit"]


@runtime_checkable
class Dimension(Protocol):
    def __mul__(self, other: Self, /) -> Self: ...
    def __truediv__(self, other: Self, /) -> Self: ...
    def __pow__(self, other: int, /) -> Self: ...

    def __rmul__(self, other: Self, /) -> Self: ...
    def __rtruediv__(self, other: Self, /) -> Self: ...

    def decompose(self) -> "dict[Dimension, int | fractions.Fraction]":
        """
        Decompose the dimension into its base dimensions and exponents.

        Notes
        -----
        By far the most common dimension system is (Length, Mass, Time, Electric
        Current, Temperature, Amount of Substance, Luminous Intensity).
        This method will decompose the dimension into a dictionary of these
        base dimensions and their respective exponents.

        Examples
        --------
        As this is an API protocol, no runtime examples are possible. The
        following is an illustrative example:

        >>> import metrology as u

        >>> dim = u.Length / u.Time

        >>> dim.decompose()
        {Length: 1, Time: -1}
        """
        ...


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
    def __eq__[B](  # type: ignore[override]  # pyright: ignore[reportIncompatibleMethodOverride]
        self: "Quantity[V, U]", other: "Quantity[op.CanEq[V, B], U]", /
    ) -> B: ...

    @override
    def __ne__[B](  # type: ignore[override]  # pyright: ignore[reportIncompatibleMethodOverride]
        self: "Quantity[V, U]", other: "Quantity[op.CanEq[V, B], U]", /
    ) -> B: ...

    def __lt__[B](
        self: "Quantity[V, U]", other: "Quantity[op.CanLt[V, B], U]", /
    ) -> B: ...
    def __le__[B](
        self: "Quantity[V, U]", other: "Quantity[op.CanLe[V, B], U]", /
    ) -> B: ...
    def __gt__[B](
        self: "Quantity[V, U]", other: "Quantity[op.CanGt[V, B], U]", /
    ) -> B: ...
    def __ge__[B](
        self: "Quantity[V, U]", other: "Quantity[op.CanGe[V, B], U]", /
    ) -> B: ...

    def __pos__[R](self: "Quantity[op.CanPos[R], U]") -> "Quantity[R, U]": ...
    def __neg__[R](self: "Quantity[op.CanNeg[R], U]") -> "Quantity[R, U]": ...
    def __abs__[R](self: "Quantity[op.CanAbs[R], U]") -> "Quantity[R, U]": ...

    def __add__[R](
        self: "Quantity[V, U]", other: "Quantity[op.CanRAdd[V, R], U]", /
    ) -> "Quantity[R, U]": ...
    def __radd__[R](
        self: "Quantity[V, U]", other: "Quantity[op.CanAdd[V, R], U]", /
    ) -> "Quantity[R, U]": ...
    def __sub__[R](
        self: "Quantity[V, U]", other: "Quantity[op.CanRSub[V, R], U]", /
    ) -> "Quantity[R, U]": ...
    def __rsub__[R](
        self: "Quantity[V, U]", other: "Quantity[op.CanSub[V, R], U]", /
    ) -> "Quantity[R, U]": ...

    def __mul__[R](
        self: "Quantity[V, U]", other: "Quantity[op.CanRMul[V, R], U]", /
    ) -> "Quantity[R, U]": ...
    def __rmul__[R](
        self: "Quantity[V, U]", other: "Quantity[op.CanMul[V, R], U]", /
    ) -> "Quantity[R, U]": ...
    def __truediv__[R](
        self: "Quantity[V, U]", other: "Quantity[op.CanRTruediv[V, R], U]", /
    ) -> "Quantity[R, U]": ...
    def __rtruediv__[R](
        self: "Quantity[V, U]", other: "Quantity[op.CanTruediv[V, R], U]", /
    ) -> "Quantity[R, U]": ...

    def __pow__[R](
        self: "Quantity[op.CanPow2[op.JustInt | op.JustFloat, R], U]",
        other: op.JustInt | op.JustFloat,
        /,
    ) -> "Quantity[R, U]": ...
    def __rpow__[R](
        self: "Quantity[op.CanRPow[op.JustInt | op.JustFloat, R], U]",
        other: op.JustInt | op.JustFloat,
        /,
    ) -> "Quantity[R, U]": ...

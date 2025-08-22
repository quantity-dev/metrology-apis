"""Metrology APIs."""

from typing import (
    Any,
    Final,
    Protocol,
    Self,
    override,
    runtime_checkable,
)

import optype as op

__version__: Final = "0.0.1.dev0"
__all__ = ["__version__", "Dimension", "MetrologyNamespace", "Quantity", "Unit"]


type VT = Any
type DT = Dimension
type UT = Unit[Any]
type QT = Quantity[Any, Any, Any]


@runtime_checkable
class MetrologyNamespace[Q: QT = QT, V: VT = VT, U: UT = UT, D: DT = DT](Protocol):
    """
    A runtime-checkable `Protocol` that defines a metrology namespace.

    The type is ``MetrologyNamespace[QT = Quantity, VT = Any, UT = Unit], DT =
    Dimension]`` where:

    - `QT` is the type of `Quantity`s. Default ``Quantity[Any, Any, Any]``.
    - `VT` is the type of values. Default ``Any``.
    - `UT` is the type of units. Default ``Unit[Any]``.
    - `DT` is the type of dimensions. Default ``Dimension[Any]``.

    Examples
    --------
    This example demonstrates a metrology namespace using placeholder functions.

    >>> from types import SimpleNamespace
    >>> mx = SimpleNamespace(asdimension=lambda x: x, asunit=lambda x: x,
    ...                      asquantity=lambda x, unit: (x, unit))

    >>> isinstance(mx.__metrology_namespace__(), MetrologyNamespace)
    True
    """

    @staticmethod
    def asdimension(obj: str | D, /) -> D:
        """
        Convert an object to a dimension.

        Parameters
        ----------
        obj : str | Dimension
            The object to convert.
        """
        ...

    @staticmethod
    def asunit(obj: str | U, /) -> U:
        """
        Convert an object to a unit.

        Parameters
        ----------
        obj : str | Unit
            The object to convert.
        """
        ...

    @staticmethod
    def asquantity(obj: Q | V, /, *, unit: U) -> Q:
        """
        Convert an object to a quantity.

        Parameters
        ----------
        obj : Quantity | Value
            The object to convert.
        unit : Unit
            The unit to use for the quantity.
        """
        ...


@runtime_checkable
class HasMetrologyNamespace[Q: QT = QT, V: VT = VT, U: UT = UT, D: DT = DT](Protocol):
    """
    A `Protocol` for metrology-aware objects.

    The type is ``HasMetrologyNamespace[QT = Quantity, VT = Any, UT = Unit, DT =
    Dimension]`` where:

    - `QT` is the type of `Quantity`s. Default ``Quantity[Any, Any, Any]``.
    - `VT` is the type of values. Default ``Any``.
    - `UT` is the type of units. Default ``Unit[Any]``.
    - `DT` is the type of dimensions. Default ``Dimension[Any]``.

    Examples
    --------
    This example demonstrates a metrology namespace using placeholder functions
    and objects.

    >>> from types import SimpleNamespace
    >>> mx = SimpleNamespace(asdimension=lambda x: x, asunit=lambda x: x,
    ...                      asquantity=lambda x, unit: (x, unit))
    >>> obj = SimpleNamespace(__metrology_namespace__=lambda: mx)

    >>> isinstance(mx.__metrology_namespace__(), MetrologyNamespace)
    True
    """

    def __metrology_namespace__(
        self, /, *, api_version: str | None = None
    ) -> MetrologyNamespace[Q, V, U, D]:
        """
        Return an object that has all the metrology API functions on it.

        Parameters
        ----------
        api_version : str or None
            String representing the version of the metrology API
            specification to be returned. If it is `None`, it should
            return the namespace corresponding to latest version of the
            metrology API specification.  If the given version is invalid
            or not implemented for the given module, an error should be
            raised. Default: `None`.

        Returns
        -------
        MetrologyNamespace
            An object representing the metrology API namespace. It
            should have every top-level function defined in the
            specification as an attribute.
        """
        ...


# ===================================================================
# Dimension


@runtime_checkable
class Dimension(Protocol):
    """
    A `Protocol` for metrology-aware Dimension objects.

    A Dimension represents a physical quantity's dimensionality, such as length, mass, or time.
    """

    # NOTE: can't inherit from HasMetrologyNamespace because of `Self` in the
    # return type.
    def __metrology_namespace__(
        self, /, *, api_version: str | None = None
    ) -> MetrologyNamespace[QT, VT, UT, Self]: ...

    def __mul__(self, other: Self, /) -> Self: ...
    def __truediv__(self, other: Self, /) -> Self: ...
    def __pow__(self, other: int, /) -> Self: ...

    def __rmul__(self, other: Self, /) -> Self: ...
    def __rtruediv__(self, other: Self, /) -> Self: ...


Dimension.__metrology_namespace__.__doc__ = (  # type: ignore[any]
    HasMetrologyNamespace.__metrology_namespace__.__doc__
)

# ===================================================================
# Unit


@runtime_checkable
class Unit[D: Dimension = Any](Protocol):
    def __metrology_namespace__(
        self, /, *, api_version: str | None = None
    ) -> MetrologyNamespace[QT, VT, Self, D]: ...

    @property
    def dimension(self) -> D: ...

    def __mul__(self, other: Self, /) -> Self: ...
    def __truediv__(self, other: Self, /) -> Self: ...
    def __pow__(self, other: int | float, /) -> Self: ...

    def __rmul__(self, other: Self, /) -> Self: ...
    def __rtruediv__(self, other: Self, /) -> Self: ...


Unit.__metrology_namespace__.__doc__ = (  # type: ignore[any]
    HasMetrologyNamespace.__metrology_namespace__.__doc__
)

# ===================================================================
# Quantity


@runtime_checkable
class Quantity[V: VT = Any, U: UT = Any, D: Dimension = Any](Protocol):
    def __metrology_namespace__(
        self, /, *, api_version: str | None = None
    ) -> MetrologyNamespace[Self, V, U, D]: ...

    @property
    def value(self) -> V: ...
    @property
    def unit(self) -> U: ...

    ### Dunder Methods

    @override
    def __eq__[B](  # type: ignore[override]  # pyright: ignore[reportIncompatibleMethodOverride]
        self: "Quantity[V, U, D]", other: "Quantity[op.CanEq[V, B], U, D]", /
    ) -> B: ...

    @override
    def __ne__[B](  # type: ignore[override]  # pyright: ignore[reportIncompatibleMethodOverride]
        self: "Quantity[V, U, D]", other: "Quantity[op.CanEq[V, B], U, D]", /
    ) -> B: ...

    def __lt__[B](
        self: "Quantity[V, U, D]", other: "Quantity[op.CanLt[V, B], U, D]", /
    ) -> B: ...
    def __le__[B](
        self: "Quantity[V, U, D]", other: "Quantity[op.CanLe[V, B], U, D]", /
    ) -> B: ...
    def __gt__[B](
        self: "Quantity[V, U, D]", other: "Quantity[op.CanGt[V, B], U, D]", /
    ) -> B: ...
    def __ge__[B](
        self: "Quantity[V, U, D]", other: "Quantity[op.CanGe[V, B], U, D]", /
    ) -> B: ...

    def __pos__[R](self: "Quantity[op.CanPos[R], U, D]") -> "Quantity[R, U, D]": ...
    def __neg__[R](self: "Quantity[op.CanNeg[R], U, D]") -> "Quantity[R, U, D]": ...
    def __abs__[R](self: "Quantity[op.CanAbs[R], U, D]") -> "Quantity[R, U, D]": ...

    def __add__[R](
        self: "Quantity[V, U, D]", other: "Quantity[op.CanRAdd[V, R], U, D]", /
    ) -> "Quantity[R, U, D]": ...
    def __radd__[R](
        self: "Quantity[V, U, D]", other: "Quantity[op.CanAdd[V, R], U, D]", /
    ) -> "Quantity[R, U, D]": ...
    def __sub__[R](
        self: "Quantity[V, U, D]", other: "Quantity[op.CanRSub[V, R], U, D]", /
    ) -> "Quantity[R, U, D]": ...
    def __rsub__[R](
        self: "Quantity[V, U, D]", other: "Quantity[op.CanSub[V, R], U, D]", /
    ) -> "Quantity[R, U, D]": ...

    def __mul__[R](
        self: "Quantity[V, U, D]", other: "Quantity[op.CanRMul[V, R], U, D]", /
    ) -> "Quantity[R, U, D]": ...
    def __rmul__[R](
        self: "Quantity[V, U, D]", other: "Quantity[op.CanMul[V, R], U, D]", /
    ) -> "Quantity[R, U, D]": ...
    def __truediv__[R](
        self: "Quantity[V, U, D]", other: "Quantity[op.CanRTruediv[V, R], U, D]", /
    ) -> "Quantity[R, U, D]": ...
    def __rtruediv__[R](
        self: "Quantity[V, U, D]", other: "Quantity[op.CanTruediv[V, R], U, D]", /
    ) -> "Quantity[R, U, D]": ...

    def __pow__[R](
        self: "Quantity[op.CanPow2[op.JustInt | op.JustFloat, R], U, D]",
        other: op.JustInt | op.JustFloat,
        /,
    ) -> "Quantity[R, U, D]": ...
    def __rpow__[R](
        self: "Quantity[op.CanRPow[op.JustInt | op.JustFloat, R], U, D]",
        other: op.JustInt | op.JustFloat,
        /,
    ) -> "Quantity[R, U, D]": ...


Quantity.__metrology_namespace__.__doc__ = (  # type: ignore[any]
    HasMetrologyNamespace.__metrology_namespace__.__doc__
)

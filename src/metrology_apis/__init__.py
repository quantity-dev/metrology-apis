"""Metrology APIs."""

from typing import Final, Protocol, Self, override, runtime_checkable

import optype as op

__version__: Final = "0.0.1.dev0"
__all__ = ["__version__", "Dimension", "Quantity", "Unit"]


@runtime_checkable
class MetrologyNamespace[Q: Quantity[V, U, D], V, U: Unit[D], D: Dimension](Protocol):

    @staticmethod
    def asdimension(obj: str | D) -> D: ...

    @staticmethod
    def asunit(obj: str | U) -> U: ...

    @staticmethod
    def asquantity(obj: Q | V, *, unit: U) -> Q: ...


@runtime_checkable
class Dimension(Protocol):
    def __metrology_namespace__[Q: Quantity, U: Unit](
        self, /, *, api_version: str | None = None
    ) -> MetrologyNamespace[Q, U, Self]:
        """
        Returns an object that has all the metrology API functions on it.
        Parameters
        ----------
        api_version: str or None
            string representing the version of the metrology API specification to be returned. If it is ``None``, it should return the namespace corresponding to latest version of the metrology API specification.  If the given version is invalid or not implemented for the given module, an error should be raised. Default: ``None``.
        Returns
        -------
        out: Any
            an object representing the metrology API namespace. It should have every top-level function defined in the specification as an attribute. It may contain other public names as well, but it is recommended to only include those names that are part of the specification.
        """

    def __mul__(self, other: Self, /) -> Self: ...
    def __truediv__(self, other: Self, /) -> Self: ...
    def __pow__(self, other: int, /) -> Self: ...

    def __rmul__(self, other: Self, /) -> Self: ...
    def __rtruediv__(self, other: Self, /) -> Self: ...


@runtime_checkable
class Unit[D: Dimension](Protocol):
    def __metrology_namespace__[Q: Quantity](
        self, /, *, api_version: str | None = None
    ) -> MetrologyNamespace[Q, Self, D]:
        """
        Returns an object that has all the metrology API functions on it.
        Parameters
        ----------
        api_version: str or None
            string representing the version of the metrology API specification to be returned. If it is ``None``, it should return the namespace corresponding to latest version of the metrology API specification.  If the given version is invalid or not implemented for the given module, an error should be raised. Default: ``None``.
        Returns
        -------
        out: Any
            an object representing the metrology API namespace. It should have every top-level function defined in the specification as an attribute. It may contain other public names as well, but it is recommended to only include those names that are part of the specification.
        """

    @property
    def dimension(self) -> D: ...

    def __mul__(self, other: Self, /) -> Self: ...
    def __truediv__(self, other: Self, /) -> Self: ...
    def __pow__(self, other: int | float, /) -> Self: ...

    def __rmul__(self, other: Self, /) -> Self: ...
    def __rtruediv__(self, other: Self, /) -> Self: ...



@runtime_checkable
class Quantity[V, U: Unit[D], D: Dimension](Protocol):
    def __metrology_namespace__(
        self, /, *, api_version: str | None = None
    ) -> MetrologyNamespace[Self, U, D]:
        """
        Returns an object that has all the metrology API functions on it.
        Parameters
        ----------
        api_version: str or None
            string representing the version of the metrology API specification to be returned. If it is ``None``, it should return the namespace corresponding to latest version of the metrology API specification.  If the given version is invalid or not implemented for the given module, an error should be raised. Default: ``None``.
        Returns
        -------
        out: Any
            an object representing the metrology API namespace. It should have every top-level function defined in the specification as an attribute. It may contain other public names as well, but it is recommended to only include those names that are part of the specification.
        """

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

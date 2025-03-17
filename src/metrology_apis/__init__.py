"""Metrology APIs."""

from typing import Final, Protocol, Self, override, runtime_checkable

import optype as op

__version__: Final = "0.0.1.dev0"
__all__ = ["__version__", "Dimension", "Quantity", "Unit"]


@runtime_checkable
class MetrologyNamespace[Q: Quantity, U: Unit, D: Dimension](Protocol):

    @staticmethod
    def asdimension(obj: str | D) -> D: ...

    @staticmethod
    def asunit(obj) -> U[D]: ...

    @staticmethod
    def asquantity(obj: V, unit: obj) -> Q[V, U[D]]: ...

    @property
    def Dimension(self) -> D: ...

    @property
    def Unit(self) -> U: ...

    @property
    def Quantity(self) -> Q: ...


@runtime_checkable
class Dimension(Protocol):
    def __metrology_namespace__(
        self, /, *, api_version: str | None = None
    ) -> MetrologyNamespace:
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
class Unit(Protocol):
    def __metrology_namespace__(
        self, /, *, api_version: str | None = None
    ) -> MetrologyNamespace:
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
    def dimension(self) -> Dimension: ...

    def __mul__(self, other: Self, /) -> Self: ...
    def __truediv__(self, other: Self, /) -> Self: ...
    def __pow__(self, other: int | float, /) -> Self: ...

    def __rmul__(self, other: Self, /) -> Self: ...
    def __rtruediv__(self, other: Self, /) -> Self: ...
    def __rpow__(self, other: int | float, /) -> Self: ...


@runtime_checkable
class Quantity[V, U: Unit](Protocol):
    def __metrology_namespace__(
        self, /, *, api_version: str | None = None
    ) -> MetrologyNamespace:
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
    def __eq__[B](self: "Quantity[V, U]", other: "Quantity[op.CanEq[V, B], U]", /) -> B: ...  # type: ignore[override]  # pyright: ignore[reportIncompatibleMethodOverride]

"""Metrology APIs."""

from typing import Any, Final, Generic, Protocol, Self, TypeVar, override, runtime_checkable

import optype as op

__version__: Final = "0.0.1.dev0"
__all__ = ["__version__", "Dimension", "Quantity", "Unit"]


VT = TypeVar('VT')
DT = TypeVar('DT', bound='Dimension')
UT = TypeVar('UT', bound='Unit[DT]')

@runtime_checkable
class MetrologyNamespace[Q: Quantity[VT, UT, DT], V, U: Unit[DT], D: Dimension](Protocol):

    @staticmethod
    def asdimension(obj: str | D) -> D: ...

    @staticmethod
    def asunit(obj: str | U) -> U: ...

    @staticmethod
    def asquantity(obj: Q | V, *, unit: U) -> Q: ...


@runtime_checkable
class Dimension(Protocol):
    def __metrology_namespace__[Q: Quantity[VT, UT, DT], V, U: Unit[DT]](
        self, /, *, api_version: str | None = None
    ) -> MetrologyNamespace[Q, V, U, Self]:
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
    def __metrology_namespace__[Q: Quantity[VT, UT, DT], V](
        self, /, *, api_version: str | None = None
    ) -> MetrologyNamespace[Q, V, Self, D]:
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
class Quantity[V, U: Unit[DT], D: Dimension](Protocol):
    def __metrology_namespace__(
        self, /, *, api_version: str | None = None
    ) -> MetrologyNamespace[Self, V, U, D]:
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
    def __eq__[B](self: "Quantity[V, U, D]", other: "Quantity[op.CanEq[V, B], U, D]", /) -> B: ...  # type: ignore[override]  # pyright: ignore[reportIncompatibleMethodOverride]

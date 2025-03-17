import pint
import metrology_apis as mt

Quantity = pint.Quantity
Unit = pint.Unit


def test_eq(q: mt.Quantity) -> None:
    print(q == q)

def test_unit(q: mt.Quantity) -> None:
    print(q.unit)

def test_value(q: mt.Quantity) -> None:
    print(q.value)

def test_m(q: mt.Quantity) -> None:
    print(q.m)


test_eq(Quantity(1, "m"))
test_unit(Quantity(1, "m"))
test_value(Quantity(1, "m"))
# test_m(Quantity(1, "m")) #error: "Quantity[Any, Any]" has no attribute "m"  [attr-defined]
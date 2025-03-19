import pint
import metrology_apis as mt
import operator as ops

Quantity = pint.Quantity
Unit = pint.Unit
# Dimension = pint.UnitsContainer


def test_dimension_op(d: mt.Dimension, op) -> None:
    print(op(d, d))


def test_dimension_pow(d: mt.Dimension) -> None:
    print(ops.pow(d, 2))


for op in [ops.mul, ops.truediv]:
    test_dimension_op(Unit("m").dimension, op)

test_dimension_pow(Unit("m").dimension)

print(isinstance(Unit("m").dimension, mt.Dimension))

def test_unit_op(u: mt.Unit, op) -> None:
    print(op(u, u))

def test_unit_pow(u: mt.Unit) -> None:
    print(ops.pow(u, 2))

for op in [ops.mul, ops.truediv]:
    test_unit_op(Unit("m"), op)

test_unit_pow(Unit("m"))


print(isinstance(Unit("m"), mt.Unit))

def test_unit(q: mt.Quantity) -> None:
    print(q.unit)

def test_value(q: mt.Quantity) -> None:
    print(q.value)


test_unit(Quantity(1, "m"))
test_value(Quantity(1, "m"))

print(isinstance(Quantity(1, "m"), mt.Quantity))

def test_op(q: mt.Quantity, op) -> None:
    print(op(q, q))


# for op in [ops.eq]:
#     test_op(Quantity(1, "m"), op)

# for op in [ops.eq, ops.ne, ops.lt, ops.le, ops.gt, ops.ge]:
#     test_op(Quantity(1, "m"), op)

# for op in [ops.add, ops.sub, ops.mul, ops.truediv]:
#     test_op(Quantity(1, "m"), op)
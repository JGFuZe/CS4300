import math
import pytest

# Get task4.py
from homework1.src import task4 

# Create Test Values for applying a discount to price
@pytest.mark.parametrize(
    "price, discount, expected",
    [
        (100, 0, 100),
        (100, 100, 0),
        (80.0, 12.5, 70.0),
        (40, 100, 0),
    ],
)

# Test if correct discount is given from a given price
def testDiscount(price, discount, expected):
    assert task4.calculateDiscount(price, discount) == expected

# Test if invalid price works
@pytest.mark.parametrize("badPrice", [-1, -0.01])
def testNegativePrice(badPrice):
    with pytest.raises(ValueError):
        task4.calculateDiscount(badPrice, 10)

# Test if invalid discount works
@pytest.mark.parametrize("badDiscount", [-0.01, -1, 100.1, 999])
def testBadDiscount(badDiscount):
    with pytest.raises(ValueError):
        task4.calculateDiscount(10, badDiscount)

# Test if non number detection works
def testNonNumber():
    with pytest.raises(TypeError):
        task4.calculateDiscount("ten", 5)
        task4.calculateDiscount(10, 'ten')
import pytest

# Get task3.py
from homework1.src import task3

# Test if signs based on given value
@pytest.mark.parametrize("n, expected", [(-5, "negative"), (0, "zero"), (7, "positive")])
def testSignOf(n, expected):
    assert task3.signOf(n) == expected

# If if first 10 primes  given correctly
def test10Primes():
    assert task3.getPrimes(10) == [2,3,5,7,11,13,17,19,23,29]

# Test if the sum to 100 is correct
def testSumToN():
    assert task3.sumToN(100) == 5050



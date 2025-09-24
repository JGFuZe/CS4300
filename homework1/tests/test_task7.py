import numpy as np
import pytest

# Get task7.py
from homework1.src import task7

# Test averaging a list
def testList():
    assert task7.calculateAverage([1, 2, 3, 4]) == 2.5

# Test averaging an array
def testNumpyArray():
    array = np.asarray([10, 20, 30], dtype=float)
    assert task7.calculateAverage(array) == 20.0

# Test averaging a tuple
def testTuple():
    assert task7.calculateAverage((3.0, 3.0, 6.0)) == 4.0

# Test if list, array, or tuple is empty
def testIfEmpty():
    with pytest.raises(ValueError):
        task7.calculateAverage([])

# Test if values in iterable are numbers
def testNonNumber():
    with pytest.raises(TypeError):
        task7.calculateAverage(["a", 2, 3])

# Test if an element in iterable is a string
def testExceptionOnString():
    with pytest.raises(TypeError):
        task7.calculateAverage("123")

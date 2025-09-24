import pytest 

# Get task2.py
from homework1.src import task2

# Test task22.py
def testTask2():
    # Using isinstance check if the function returns are the correct data type
    assert isinstance(task2.getInt(), int)
    assert isinstance(task2.getFloat(), float)
    assert isinstance(task2.getString(), str)
    assert task2.getBoolean() == True

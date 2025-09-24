# Get task5.py
from homework1.src import task5

def testBooks():
    # Test if # of books is 5 or more
    assert len(task5.books) >= 5

    # Get first 3 books
    first3 = task5.firstThreeBooks()

    # Test if first three books of structure is 3
    assert len(first3) == 3

    # Test if title and author is in all the first 3's elements
    assert all(("title" in b and "author" in b) for b in first3)

def testStudentLookup():
    # Test if getting student's id works
    assert task5.getStudentId("Alice")

    # Test if putting an non-existent student returns None
    assert task5.getStudentId("who?") == None

    # Check if both key and value are strings
    assert "Bob" in task5.studentDB and isinstance(task5.getStudentId("Bob"), str)

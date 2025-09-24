from pathlib import Path
import pytest

# Get task6.py
from homework1.src import task6

# Test word count
def testWordCount(tmp_path: Path):
    assert task6.countWordsInFile("/home/student/CS4300-Code/homework1/task6_read_me.txt") == 104

# Test if file was found
def testFileNotFound():
    with pytest.raises(FileNotFoundError):
        task6.countWordsInFile("idk_bob.txt")

# Metaprogramming check: decorator added attribute & increments
def testCallCounterIncrements():
    assert hasattr(task6.countWordsInFile, "callCount")
    before = task6.countWordsInFile.callCount

    task6.countWordsInFile("/home/student/CS4300-Code/homework1/task6_read_me.txt")

    assert task6.countWordsInFile.callCount == before + 1

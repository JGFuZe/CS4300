
# Get task1.py
from homework1.src import task1

# Test task1.py
def testTask1(capsys):

    # Run task1.py
    task1.main()

    # Test if output is correct
    assert capsys.readouterr().out.strip() == "Hello, World!"

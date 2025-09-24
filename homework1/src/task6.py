from pathlib import Path
from functools import wraps

# Decorator: add a call counter to the function (metaprogramming).
def countCalls(func):
    
    @wraps(func)
    def wrapper(*args, **kwargs):

        # Increment call counter
        wrapper.callCount += 1
        return func(*args, **kwargs)

    # Init counter on the wrapper
    wrapper.callCount = 0 

    # Return wrapped function
    return wrapper

@countCalls
def countWordsInFile(path: str | Path) -> int:
    # Get file
    file = Path(path)

    try:
        # This is the operation that can raise FileNotFoundError
        text = file.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"File at {file} not found") from exc

    # Split words on whitespace
    words = text.split()

    # Return length of words (int)
    return len(words)

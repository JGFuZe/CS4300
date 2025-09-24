import numpy as np

# Calculate the average of all the elements of a numeric list, array, or tuple
def calculateAverage(values):

    # test for string-like inputs
    if isinstance(values, (str, bytes, bytearray)):
        raise TypeError("values must be an iterable of numeric types")

    try:
        # Create numpy array
        array = np.asarray(values, dtype=float)
    except Exception as exc:
        # Raise exception if a non-number
        raise TypeError("values must be an iterable of numeric types") from exc

    # Raise error if array is empty
    if array.size == 0:
        raise ValueError("values must not be empty")

    # If not return the average of all the values in the array
    return float(np.mean(array))

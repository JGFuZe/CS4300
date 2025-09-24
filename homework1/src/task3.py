
# Return if number is pos, neg, or zero in a string
def signOf(n) -> str:
    if n > 0:
        return "positive"
    elif n < 0:
        return "negative"
    return "zero"

# Check if given arg is a prime number
def isPrime(x) -> bool:
    if x < 2:
        return False
    if x in (2, 3):
        return True
    if x % 2 == 0:
        return False

    # trial division
    i = 3
    while i * i <= x:
        if x % i == 0:
            return False
        i += 2
    return True

# Get prime numbers in a desired range
def getPrimes(k):
    found = [] # Array of found primes

    # Start with 2 because no primes below 2
    candidate = 2

    # Test for primes up til k (10 for this)
    for _ in range(10**6): # Big range

        # Test if candidate is a prime
        if (isPrime(candidate)):
            #If new prime is found, then add it to array
            found.append(candidate)

            # Test if desired # of primes
            if len(found) >= k:
                break 
            
        candidate += 1
    return found

# Add together all number up to n
def sumToN(n):
    total = 0
    i = 1

    while (i <= n):
        total += i
        i += 1
    return total

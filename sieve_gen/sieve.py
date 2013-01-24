_primelist = [2]

def _is_prime(primes, n):
    for i in primes:
        if n % i == 0:
            return False

    return True

def next():
    start = _primelist[-1] + 1
    while 1:
        if _is_prime(_primelist, start):
            _primelist.append(start)
            yield start

        start += 1
        

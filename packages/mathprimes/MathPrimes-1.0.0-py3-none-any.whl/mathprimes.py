from typing import Tuple, Generator


__all__ = ("is_prime", "prime_factorization")


def _is_prime(i: int, prev: Tuple[int]) -> bool:
    """
    Returns whether or not an integer is prime.
    Uses the fact that all prime numbers except two and three are one more or one less than a multiple of six.
    The checks whether a given list of smaller primes are factors.
    If not then the number is prime.
    """
    
    if i in {0,1}:
        return False
    if i in {2,3}:
        return True
    if (i - 1) % 6 == 0 or (i + 1) % 6 == 0:
        for j in prev:
            if i % j == 0:
                return False
        return True
    return False


def prime_gen() -> Generator[Tuple[int,Tuple[int]], None, None]:
    """An infinite generator yielding a tuple of ``(prime_number, previous_prime_numbers)``"""
    primes = ()
    i = 2
    while True:
        if _is_prime(i, primes):
            primes += (i,)
            yield i, primes
        i += 1


def is_prime(number: int, primes = None) -> bool:
    """A function that implents ``_is_prime`` from above but will auto generate primes if not given."""
    if primes is None:
        for i, primes in prime_gen():
            if i >= number:
                break
    return number in primes


def prime_factorization(number: int, primes = None):
    """
    Given any integer and an optional iterable of primes.
    Returns a dictionary of the prime factors and their occurences.
    """
    if number <= 1:
        return None
    # If primes is not given autogenerate them.
    if primes is None:
        for i, primes in prime_gen():
            if i >= number:
                break
    for prime in primes:
        if number % prime == 0:
            if (next_number := number // prime) == 1:
                return {prime: 1}
            result = prime_factorization(next_number, primes)
            if result.get(prime):
                result[prime] += 1
            else:
                result[prime] = 1
            return result
    raise ValueError(f"Not supposed to happen? {number}")


if __name__ == "__main__":
    def main():
        print(is_prime(1669))
        print(prime_factorization(8345))
        
    main()
    
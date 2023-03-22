def factorial_recursive(n: int) -> int:
    """Original recursive function."""
    if n < 2:
        return 1
    return n * factorial_recursive(n - 1)


def factorial_iterative(n: int, result: int = 1) -> int:
    """Iterative function."""
    while True:
        if n < 2: break
        (n, result) = (n-1, n * result)
    return result


if __name__ == "__main__":
    print(factorial_recursive(n=5))
    print(factorial_iterative(n=5))

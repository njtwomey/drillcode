from collections import Counter


def validate(result, case, scaffolds):
    s = case["input"]["s"]
    if not isinstance(result, str):
        return False, f"expected a string, got {type(result).__name__}"
    # Impossible exactly when one letter needs more than ceil(n / 2) slots.
    possible = max(Counter(s).values()) <= (len(s) + 1) // 2
    if not possible:
        return (result == "", f"no arrangement exists, expected an empty string, got {result!r}")
    if result == "":
        return False, "an arrangement exists but an empty string was returned"
    if Counter(result) != Counter(s):
        return False, f"{result!r} does not use exactly the letters of {s!r}"
    for a, b in zip(result, result[1:]):
        if a == b:
            return False, f"{result!r} has two adjacent {a!r}"
    return True, ""

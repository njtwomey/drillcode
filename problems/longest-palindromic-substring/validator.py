def validate(result, case, scaffolds):
    s = case["input"]["s"]
    expected = case["expected"]
    if not isinstance(result, str):
        return False, f"expected a string, got {type(result).__name__}"
    if result not in s:
        return False, f"{result!r} is not a substring of {s!r}"
    if result != result[::-1]:
        return False, f"{result!r} is not a palindrome"
    if len(result) != len(expected):
        return False, f"expected length {len(expected)}, got {len(result)}"
    return True, ""

def validate(result, case, scaffolds):
    original = case["input"]["nums"]
    unique = sorted(set(original))
    if result != len(unique):
        return False, f"returned k={result!r}, expected {len(unique)}"
    nums = case["args"]["nums"]
    if nums[:result] != unique:
        return False, f"first {result} elements are {nums[:result]}, expected {unique}"
    return True, ""

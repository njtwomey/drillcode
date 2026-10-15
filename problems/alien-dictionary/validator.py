def validate(result, case, scaffolds):
    words = case["input"]["words"]
    expected = case["expected"]
    if not isinstance(result, str):
        return False, f"expected a string, got {type(result).__name__}"
    if expected == "":
        return (result == ""), "no valid order exists, expected an empty string"
    letters = {c for w in words for c in w}
    if result == "":
        return False, "a valid order exists but got an empty string"
    if len(result) != len(set(result)) or set(result) != letters:
        return False, f"order must contain each of {sorted(letters)} exactly once"
    pos = {c: i for i, c in enumerate(result)}
    for a, b in zip(words, words[1:]):
        for x, y in zip(a, b):
            if x != y:
                if pos[x] > pos[y]:
                    return False, f"{a!r} must come before {b!r}, but {x!r} is after {y!r}"
                break
    return True, ""

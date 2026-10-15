import random
from collections import Counter


def validate(result, case, scaffolds):
    w = case["args"]["w"]
    total = sum(w)
    obj = case["entry"](w)
    random.seed(0)
    draws = 20000
    counts = Counter()
    for _ in range(draws):
        idx = obj.pickIndex()
        if not isinstance(idx, int) or not 0 <= idx < len(w):
            return False, f"pickIndex returned {idx!r}, not an index in 0..{len(w) - 1}"
        counts[idx] += 1
    for i, weight in enumerate(w):
        want = weight / total
        got = counts[i] / draws
        if abs(got - want) > 0.03:
            return False, f"index {i}: picked {got:.3f} of the time, expected about {want:.3f}"
    return True, ""

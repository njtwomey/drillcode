import math


def validate(result, case, scaffolds):
    n = case["input"]["n"]
    bad = case["input"]["bad"]
    calls = []

    def is_bad(version):
        calls.append(version)
        return version >= bad

    # The solution is exec'd in its own namespace; inject the judge API there.
    case["entry"].__func__.__globals__["isBadVersion"] = is_bad
    answer = case["entry"](n)
    if answer != bad:
        return False, f"expected first bad version {bad}, got {answer!r}"
    limit = 2 * math.ceil(math.log2(n + 1)) + 2
    if len(calls) > limit:
        return False, f"isBadVersion called {len(calls)} times; expected at most {limit} (not a binary search)"
    return True, ""

from collections import Counter


def validate(result, case, scaffolds):
    nums1 = case["input"]["nums1"]
    nums2 = case["input"]["nums2"]
    k = case["input"]["k"]
    if not isinstance(result, list):
        return False, f"expected a list of pairs, got {type(result).__name__}"
    # The best k sums, computed by brute force from the inputs.
    best = sorted(a + b for a in nums1 for b in nums2)[:k]
    if len(result) != len(best):
        return False, f"expected {len(best)} pairs, got {len(result)}"
    c1, c2 = Counter(nums1), Counter(nums2)
    used = Counter()
    for pair in result:
        if not isinstance(pair, list) or len(pair) != 2:
            return False, f"{pair!r} is not a pair"
        a, b = pair
        if c1[a] == 0 or c2[b] == 0:
            return False, f"{pair!r} is not a pair of one value from each array"
        used[(a, b)] += 1
        # Duplicate values give several distinct index pairs with the same values.
        if used[(a, b)] > c1[a] * c2[b]:
            return False, f"pair {pair!r} is used more often than it exists"
    if sorted(a + b for a, b in result) != best:
        return False, "the sums of the returned pairs are not the k smallest sums"
    return True, ""

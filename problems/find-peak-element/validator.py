def validate(result, case, scaffolds):
    nums = case["args"]["nums"]
    n = len(nums)
    if not isinstance(result, int) or isinstance(result, bool):
        return False, f"expected an integer index, got {result!r}"
    if not 0 <= result < n:
        return False, f"index {result} is out of range for length {n}"
    inf = float("inf")
    left = nums[result - 1] if result > 0 else -inf
    right = nums[result + 1] if result < n - 1 else -inf
    if nums[result] > left and nums[result] > right:
        return True, ""
    return False, f"index {result} (value {nums[result]}) is not strictly greater than both neighbours"

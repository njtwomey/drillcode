## The idea

The slow way asks, for every element, "what is the longest increasing run that ends here?" and checks every earlier element to find out. That is O(n²).

The faster way keeps one small list, `tails`, and asks a cleverer question: for each length, what is the smallest value an increasing run of that length could end with? A smaller ending is always better, because it leaves more room to keep growing. Once you hold only the best ending per length, the list is automatically sorted, and sorted lists can be searched with binary search.

## Set-up

- `tails` starts empty. `tails[i]` is the smallest possible last value of an increasing subsequence of length `i + 1`.
- Invariant: `tails` is strictly increasing. Its length is the answer so far. Its contents are not a real subsequence, only a record of best endings.

```text
nums  = [3, 5, 6, 2, 4, 7]
tails = []
```

## Step by step

For each `num`, `bisect_left(tails, num)` returns the first slot whose value is `>= num`. If that slot is past the end, `num` extends the longest run. Otherwise `num` overwrites the slot: same length, smaller ending.

```text
num   slot i   action                    tails
 3      0      i == len -> append        [3]
 5      1      i == len -> append        [3, 5]
 6      2      i == len -> append        [3, 5, 6]
 2      0      replace tails[0]          [2, 5, 6]
 4      1      replace tails[1]          [2, 4, 6]
 7      3      i == len -> append        [2, 4, 6, 7]
```

The answer is `len(tails)`, which is 4 (for example 3, 5, 6, 7). Notice that after `4` the list reads `[2, 4, 6]`, yet `2` appeared after `6` in the input. So `tails` is not itself a subsequence. The `2` and `4` only say "a length-1 run can end as low as 2, a length-2 run as low as 4". That is what let `7` extend a length-3 run.

## Why it works

Every replacement keeps a length's ending as small as it can be, and a smaller ending can only help later numbers. Because endings for longer runs are never smaller than endings for shorter ones, `tails` stays sorted, so the binary search is valid. A new longest run appears exactly when a number beats every ending.

## Where it goes wrong

Use `bisect_left`, not `bisect_right`. With duplicates, `bisect_right` would append an equal value and count a non-strict run.

```text
nums = [2, 2, 2]
bisect_left : [2] -> [2] -> [2]          answer 1
bisect_right: [2] -> [2, 2] -> [2, 2, 2] answer 3  (wrong)
```

Returning `tails` as the subsequence is the other trap: only its length is meaningful.

## Other approaches

`lengthOfLISQuadratic` fills `dp[i]` = longest run ending exactly at `nums[i]` by looking at every `j < i` with a smaller value, then takes the max. It is simpler to reason about and O(n²) time, O(n) space.

## Cost

Time O(n log n): one binary search per number. Space O(n) for `tails` in the worst case (a fully increasing input).

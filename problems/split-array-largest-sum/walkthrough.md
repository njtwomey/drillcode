## The idea

Trying every way to cut the array into `k` pieces is exponential. Flip the question: instead of "what is the best split?", ask "can I split so that no piece sums above `cap`?" That question is easy to answer greedily: keep adding numbers to the current piece, and start a new piece only when the next number would overflow `cap`. The count of pieces this makes is the fewest possible for that cap.

The answer to the original problem is the smallest `cap` for which that fewest count is at most `k`. A larger cap never needs more pieces, so feasibility goes from "no" to "yes" at one threshold. That is exactly the shape binary search needs.

## Set-up

- `pieces_needed(cap)` runs the greedy: `count` starts at 1, `total` is the running sum of the current piece.
- `lo = max(nums)`: a cap below the biggest element cannot hold it.
- `hi = sum(nums)`: with that cap one piece is enough (`k = 1`), so it is always feasible.
- The loop keeps the answer within `[lo, hi]`.

If the greedy needs fewer than `k` pieces, we can split pieces further without raising any sum (non-empty subarrays are available because `k <= len(nums)`), so "at most `k`" is the right test.

```text
nums = [7, 2, 5, 10, 8]    k = 2
lo = 10 (max)              hi = 32 (sum)

 10 ........................................ 32
 lo                                          hi
```

## Step by step

```text
lo=10 hi=32  mid=21  [7,2,5] [10,8]       2 pieces (sums 14, 18)
                     feasible: hi = 21
lo=10 hi=21  mid=15  [7,2,5] [10] [8]     3 pieces > 2
                     too small: lo = 16
lo=16 hi=21  mid=18  [7,2,5] [10,8]       2 pieces
                     feasible: hi = 18
lo=16 hi=18  mid=17  [7,2,5] [10] [8]     3 pieces
                     too small: lo = 18
lo=18 hi=18  stop, answer 18
```

The split `[7,2,5] [10,8]` has sums 14 and 18, so the largest is 18. With cap 17 the `10` and `8` cannot share a piece (18 > 17), forcing a third piece.

## Why it works

Greedy is optimal for a fixed cap: delaying a cut never hurts, because a later cut leaves later pieces with less work. So `pieces_needed` is the true minimum. Monotonicity makes the binary search find the smallest feasible cap, and the smallest feasible cap is the minimised largest sum, since a split exists whose max piece equals it.

## Where it goes wrong

- Setting `lo = 0` or `1` lets `mid` fall below an element, and the greedy then miscounts.
- Using `lo = mid` instead of `mid + 1` on failure loops forever.
- Treating "exactly `k`" as the test: use `<= k`.

## Cost

Time O(n log(sum)): about log of the range binary-search steps, each a linear greedy pass. Space O(1).

## Other approaches

DP over (position, pieces used) with prefix sums is O(n^2 * k). It is fine for these limits but slower than the binary search.

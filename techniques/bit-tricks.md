---
title: Bit tricks
area: Bits
topics: [Bit manipulation]
problems:
  - number-of-1-bits
  - counting-bits
  - missing-number
  - reverse-bits
  - sum-of-two-integers
  - subsets
related: [backtracking-template, dp-space-and-loop-order]
---
## Reach for it when

- The statement mentions bits, binary, parity, set bits, powers of two or a 32-bit integer.
- It forbids arithmetic operators such as `+`.
- Every value appears twice except one, or one value in a range is missing, and O(1) extra space is required.
- The input is a small set (about 20 elements or fewer) and every subset must be visited.
- An answer for `i` follows from the answer for a smaller number with fewer bits.

## Setup

- `n` or `a`, `b`: the integers. Python integers are unbounded and negatives never wrap, so any problem that fixes a width needs `mask = 0xFFFFFFFF` and a round count that does not depend on the value.
- `count = 0` for set bits. Invariant: `count` is the number of bits already cleared from `n`.
- `result = 0` for an XOR accumulator or a rebuilt number. Invariant: for XOR, `result` is the XOR of everything seen; for a rebuilt number, it holds the bits read so far in their final positions.
- `mask` as a loop variable over `range(1 << n)` for subsets. Invariant: bit `i` of `mask` says whether element `i` is included, and each mask in the range is a distinct subset.
- The facts the loops lean on:
  - `n & (n - 1)` clears the lowest set bit.
  - `n & -n` isolates the lowest set bit.
  - `a ^ a == 0` and `a ^ 0 == a`, and XOR is order-independent.
  - `i >> 1` drops the last bit and `i & 1` reads it.

## Template

```python
def bit_tricks(n):
    count = 0
    rest = n
    while rest:
        rest &= rest - 1
        count += 1
    return count, count == 1, n & -n
```

`bit_tricks(12)` returns `(2, False, 4)` and `bit_tricks(8)` returns `(1, True, 8)`: the set-bit count, whether `n` is a power of two (exactly one set bit), and the lowest set bit. The loop runs once per set bit, not once per bit position.

## What it removes

- A loop over all 32 positions when only the set bits matter.
- A hash set or sorting to find a missing or unpaired value. XOR cancels pairs in O(n) time and O(1) space and cannot overflow.
- Recounting from scratch in counting bits. Each answer reuses a smaller, already computed one.
- The `+` operator, using XOR for the digit sum and AND-shift for the carry.
- Include/exclude recursion for subsets, when a counter from 0 to `2^n - 1` names every subset.

## Pitfalls

- Looping `while n` in reverse bits. Leading zeros must become trailing zeros, so a number like `1` loses its shift positions. Run exactly 32 rounds.
- Not masking in the addition problem. With a negative argument the carry never reaches zero in Python and the loop does not end. Mask `a`, `b` and each new value to 32 bits.
- Forgetting to convert back at the end of that problem. If the result is above `0x7FFFFFFF`, bit 31 is set; return `~(a ^ mask)` to get the negative value.
- Operator precedence. `mask >> i & 1` parses as `(mask >> i) & 1`, which is what is wanted, but `n & 1 == 0` parses as `n & (1 == 0)`. Parenthesise comparisons.
- Starting the missing-number XOR at 0 instead of `len(nums)`. The answer is wrong when the missing number is `n`, since no index equals it.
- Using `n & (n - 1) == 0` for a power-of-two test without excluding `n == 0`.
- Treating the input as signed when the problem says unsigned. The count loop on a Python negative never ends; in this catalogue inputs are non-negative.

## Variants

- Count set bits, `number-of-1-bits`: `n &= n - 1` until zero, counting the rounds.
- Bit counts for 0..n, `counting-bits`: `dp[i] = dp[i >> 1] + (i & 1)` or `dp[i] = dp[i & (i - 1)] + 1`. Both use an answer for a smaller index already in `dp`.
- Pairs cancel, `missing-number`: start `result = len(nums)`, XOR every index and every value; the missing number remains. The sum formula `n(n+1)/2 - sum(nums)` is the alternative.
- Fixed-width reversal, `reverse-bits`: 32 rounds of `result = (result << 1) | (n & 1)` then `n >>= 1`.
- Addition without `+`, `sum-of-two-integers`: `a ^ b` is the sum without carries, `(a & b) << 1` is the carry; repeat until the carry is zero, masking to 32 bits each round.
- Enumerate subsets, `subsets`: for each `mask` in `range(1 << n)`, include `nums[i]` when `mask >> i & 1`. The include/exclude recursion in the same file is the backtracking form; see `backtracking-template`.

## Worked example

Problem: `sum-of-two-integers`

XOR for the sum, AND-shift for the carry, and a 32-bit mask to emulate two's complement.

```python
class Solution:

    def getSum(self, a: int, b: int) -> int:
        mask = 4294967295
        a &= mask
        b &= mask
        while b:
            a, b = ((a ^ b) & mask, (a & b) << 1 & mask)
        return a if a <= 2147483647 else ~(a ^ mask)
```

`mask` holds the 32-bit width. Both inputs are masked first, so a negative argument becomes its unsigned form. Inside the loop `a ^ b` is the sum without carries and `(a & b) << 1` is the carry, both masked. The carry rises at least one position per round, so the loop ends within 32 rounds. The last line is the pitfall from above: if bit 31 is set, `~(a ^ mask)` turns the unsigned value back into a Python negative.

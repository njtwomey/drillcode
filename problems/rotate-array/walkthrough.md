## The idea

Rotating right by `k` means the last `k` elements jump to the front, keeping their order, and the rest follow in their order. Doing it with a copy is easy but takes O(n) space. In place, the trick is three reversals.

Reverse the whole array. The last `k` elements are now at the front, but backwards, and the first `n - k` elements are at the back, also backwards. Reversing each block on its own puts each back in its original order.

## Set-up

- `n` is the length.
- `k %= n` first. Rotating by `n` changes nothing, so only the remainder matters. This also makes `k` larger than `n` safe, and a `k` of zero stays a no-op.
- `reverse(lo, hi)` swaps from both ends toward the middle, in place.

```text
nums = [1, 2, 3, 4, 5, 6, 7]    k = 3

 index  0  1  2  3  4  5  6
        1  2  3  4  5  6  7
        └ n - k = 4 ┘└ k = 3 ┘
```

## Step by step

```text
start                 [1, 2, 3, 4, 5, 6, 7]

reverse(0, 6)         [7, 6, 5, 4, 3, 2, 1]
                       └ k ─┘ └─ n - k ──┘
                       the last 3, backwards, now lead

reverse(0, 2)         [5, 6, 7, 4, 3, 2, 1]
                       first block restored

reverse(3, 6)         [5, 6, 7, 1, 2, 3, 4]
                       second block restored
```

The result `[5, 6, 7, 1, 2, 3, 4]` is the original rotated right by 3.

## Why it works

Reversal is its own inverse. After the first step, the block `[5, 6, 7]` sits at the front, but as `[7, 6, 5]`. Reversing that block undoes the backwards order. The same holds for the other block. The full reversal does the moving, and the two small reversals fix the ordering.

## Where it goes wrong

- Skipping `k %= n`. With `k > n` the block bounds fall outside the array, and with `k = n` the first block would be the whole array, then reversed again.
- Mixing up the bounds. The blocks are `0..k-1` and `k..n-1`. Using `k` for the first block's end shifts everything by one.
- `k = 0` is safe: `reverse(0, -1)` does nothing, and the other two reversals are the same range, so they cancel out.

## Other approaches

Copy into a new array placing each element at `(i + k) % n`. That is simple but costs O(n) space. A cyclic-replacement method moves each element straight to its target and follows cycles, also O(1) space, but the cycle counting is fiddlier than three reversals.

## Cost

Time O(n): every element is swapped at most twice across the three reversals. Space O(1): the swaps use no extra array.

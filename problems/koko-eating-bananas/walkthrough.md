## The idea

We want the smallest eating speed that finishes all piles within `h` hours. The tricky part is that the answer is not in the input, but we can test any candidate speed easily: count hours as the sum of `ceil(pile / speed)`. And testing is monotonic. If speed 5 is fast enough, so is 6, 7 and every higher speed. If it is too slow, so is everything lower.

A monotonic yes/no across a range is exactly what binary search needs. We search over speeds, not over the piles.

## Set-up

- `lo = 1`: speed 0 is meaningless.
- `hi = max(piles)`: this speed always works, since each pile takes one hour and `h >= len(piles)`. Going faster than the biggest pile never helps.
- Invariant: the answer lies in `[lo, hi]`.
- `(pile + mid - 1) // mid` is an integer ceiling. A partial pile still costs a whole hour, since Koko does not move on to the next pile in the same hour.

```text
piles = [3, 6, 7, 11]    h = 8

speed:   1 2 3 4 5 6 7 8 9 10 11
         ^lo                  ^hi
```

## Step by step

```text
lo=1  hi=11  mid=6   hours: 1+1+2+2 = 6    <= 8  feasible -> hi = 6
lo=1  hi=6   mid=3   hours: 1+2+3+4 = 10   >  8  too slow  -> lo = 4
lo=4  hi=6   mid=5   hours: 1+2+2+3 = 8    <= 8  feasible -> hi = 5
lo=4  hi=5   mid=4   hours: 1+2+2+3 = 8    <= 8  feasible -> hi = 4
lo=4  hi=4   stop, return 4
```

```text
speed:    1  2  3  4  5  6  7 ...
feasible: no no no YES YES YES YES ...
                    ^ the single flip point that we find
```

## Why it works

Feasibility flips once from "no" to "yes" as speed grows. When `mid` is feasible, the answer is `mid` or something smaller, so `hi = mid` keeps it. When `mid` is not feasible, so is every smaller speed, so `lo = mid + 1` drops them. The range shrinks until it holds one value, the smallest feasible speed.

## Where it goes wrong

- Setting `hi = mid - 1` on a feasible speed throws away a possible answer. It must stay as `hi = mid`, which is why the loop is `lo < hi` and not `lo <= hi`.
- Using `pile // mid` floors and undercounts the hours for partial piles. The ceiling is essential.
- Searching from 0 would divide by zero.

## Cost

Time O(n log m) where `m = max(piles)`: about log m rounds, each summing over `n` piles. Space O(1).

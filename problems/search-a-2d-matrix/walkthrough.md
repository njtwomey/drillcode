## The idea

The matrix has two promises: every row is sorted, and each row starts above the last value of the row before it. Put those together and reading the grid row by row gives one long sorted list. So there is no need for a clever two-stage search (find the row, then find the column). One ordinary binary search over the whole thing does it.

The catch is that we do not want to build that long list, since copying it would cost O(m·n). Instead we pretend it exists and translate each index on demand. Flat index `i` lives at row `i // cols` and column `i % cols`.

## Set-up

- `rows`, `cols` are the grid dimensions. `cols` is the divisor that turns a flat index into a position.
- `lo`, `hi` are the flat indices of the live range, starting at `0` and `rows * cols - 1`. Invariant: if `target` is present at all, its flat index is inside `[lo, hi]`.

```text
matrix (rows=3, cols=4)          flat view (index -> value)

  1  3  5  7                      0  1  2  3  4   5   6   7   8  9  10 11
 10 11 16 20                      1  3  5  7  10 11  16  20  23 30  34 60
 23 30 34 60                      ^lo                                 ^hi
```

## Step by step

Search for `target = 16`. Each round computes `mid`, maps it to `(mid // cols, mid % cols)` and compares.

```text
Round 1   lo=0  hi=11  mid=5   -> row 1, col 1 -> value 11
          11 < 16, target is to the right:  lo = mid + 1 = 6

           1  3  5  7
          10 [11] 16 20        <- mid
          23 30 34 60

Round 2   lo=6  hi=11  mid=8   -> row 2, col 0 -> value 23
          23 > 16, target is to the left:   hi = mid - 1 = 7

           1  3  5  7
          10 11 16 20
          [23] 30 34 60        <- mid

Round 3   lo=6  hi=7   mid=6   -> row 1, col 2 -> value 16
          16 == 16, return True

           1  3  5  7
          10 11 [16] 20        <- mid
          23 30 34 60
```

If the target were `13`, the range would keep shrinking until `lo > hi`, and the function would return `False`.

## Why it works

Binary search only needs a sorted sequence and a way to read item `i` cheaply. The row-major order is sorted because each row is sorted and each row's first value beats the previous row's last. Reading item `i` is O(1) with one division and one remainder. Every round throws away the half that cannot hold `target`, so the invariant on `[lo, hi]` holds until the range is empty.

## Where it goes wrong

- Mixing up the divisor. Row is `mid // cols`, not `mid // rows`. A non-square grid exposes this at once.

```text
rows=2, cols=4, mid=5
right: row 5 // 4 = 1, col 5 % 4 = 1
wrong: row 5 // 2 = 2  -> index out of range
```

- Using `lo < hi` instead of `lo <= hi`. A one-cell range (`lo == hi`) still needs checking, and the single-element grid `[[1]]` would return `False`.
- Searching rows first, then columns, works but is two searches and more edge cases (target below the first value, target between rows).

## Cost

Time O(log(m·n)) since the range halves each round. Space O(1): the flat list is never built.

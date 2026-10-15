## The idea

Both lists are sorted and each list's intervals do not overlap each other. That means we never have to compare every pair: with a pointer in each list we only compare the two current intervals, record their overlap if any, then discard whichever ends first, because it cannot overlap anything later in the other list.

## Set-up

- `i` points into `firstList`, `j` into `secondList`, both starting at 0.
- `lo = max(starts)` and `hi = min(ends)` describe the overlap of the two current intervals. If `lo <= hi` the overlap is real.
- `result` collects the overlaps in order.

Invariant: every overlap involving an interval before `i` or before `j` has already been recorded.

```text
first : [0,2]  [5,10]  [13,23]  [24,25]
         ^ i
second: [1,5]  [8,12]  [15,24]  [25,26]
         ^ j
```

## Step by step

```text
 i  j   first    second   lo  hi   overlap?   advance
 0  0   [0,2]    [1,5]     1   2   [1,2]      2<5   -> i
 1  0   [5,10]   [1,5]     5   5   [5,5]      10<5? no -> j
 1  1   [5,10]   [8,12]    8  10   [8,10]     10<12 -> i
 2  1   [13,23]  [8,12]   13  12   none       23<12? no -> j
 2  2   [13,23]  [15,24]  15  23   [15,23]    23<24 -> i
 3  2   [24,25]  [15,24]  24  24   [24,24]    25<24? no -> j
 3  3   [24,25]  [25,26]  25  25   [25,25]    25<26 -> i
 4         i is past the end, loop stops
```

Result: `[[1,2], [5,5], [8,10], [15,23], [24,24], [25,25]]`.

The sixth row shows why we advance the one that ends first. `[24,25]` is kept because it ends later than `[15,24]`, so it might still meet `[25,26]`, which it does.

```text
number line, rows 6-7:
   15        24 25 26
   ├──────────┤          second[2] = [15,24]
             ├─┤          first[3]  = [24,25]   overlap [24,24]
               ├─┤        second[3] = [25,26]   overlap [25,25]
```

## Why it works

The interval that ends first has no future: the other list's later intervals start after the other current interval ends, and that is no earlier than this one's end. So nothing later can reach it, and dropping it loses nothing. In the tie case the code advances `j`; the other interval then gets compared with the next one, which is harmless.

## Where it goes wrong

- Using `lo < hi` drops single-point overlaps such as `[5,5]`. Touching endpoints count, so it is `lo <= hi`.
- Advancing the interval that ends later, or both always. You would skip overlaps, for example `[24,25]` against `[25,26]` above.
- If either list is empty the loop never runs and the result is `[]`, which is correct.

## Cost

Time O(m + n): every step advances one pointer, so there are at most m + n steps. Space O(1) beyond the output.

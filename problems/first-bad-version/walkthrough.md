## The idea

Versions are numbered 1 to `n`; once one is bad, every later one is bad too. So `isBadVersion` is false, false, ..., false, true, true, ..., true, and we want the first true. That is a sorted structure, so binary search applies: probe the middle, and one answer tells you which half to discard. It also keeps API calls to about log2(n).

## Set-up

- `lo` and `hi` bound the range that must contain the answer. They start at `1` and `n`.
- `mid` is the version being tested.

Invariant: the first bad version is always within `lo..hi`. The loop runs while `lo < hi` and ends when exactly one candidate remains, which must be it. The problem guarantees at least one bad version, so the range is never empty of answers.

```text
version:   1   2   3   4   5
isBad:     F   F   F   T   T
           ^               ^
           lo              hi
```

## Step by step

```text
Round 1   mid = 1 + (5 - 1) // 2 = 3     isBadVersion(3) = False
          mid is good, so lo = mid + 1 = 4

version:   1   2   3   4   5
                       ^   ^
                       lo  hi

Round 2   mid = 4 + (5 - 4) // 2 = 4     isBadVersion(4) = True
          mid may be the first bad one, so hi = mid = 4

version:   1   2   3   4   5
                       ^
                    lo = hi

lo < hi is false, return 4.
```

## Why it works

If `mid` is good, then all versions up to `mid` are good and the answer is above it, so `lo = mid + 1` loses nothing. If `mid` is bad, the answer is `mid` or earlier, so `hi = mid` keeps it. Either way the invariant holds and the range shrinks every round.

## Where it goes wrong

Setting `hi = mid - 1` when `mid` is bad discards a version that might be the answer:

```text
version:   1   2   3   4   5     first bad = 4
                       ^
lo=4 hi=5 mid=4 is bad: hi = 3 -> now lo > hi, answer lost
```

The shape here is "keep mid on the bad side", which pairs with `while lo < hi`. Pairing it with `lo <= hi` and `hi = mid` can loop forever once `lo == hi`.

## Cost

Time O(log n) calls to `isBadVersion`. Space O(1).

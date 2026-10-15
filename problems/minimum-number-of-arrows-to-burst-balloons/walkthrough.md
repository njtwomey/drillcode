## The idea

Each balloon is an interval on a number line, and an arrow at position `x` pops every balloon whose interval contains `x`. We want the fewest arrows. Trying every candidate position for every balloon is a mess. Greedy makes it simple: look at the balloon that ends first. Some arrow has to pop it, and the best place for that arrow is at its right edge. Any arrow further left inside it can only lose balloons that start after the new position, and an arrow at the right edge catches everything that starts at or before that edge and is still alive there.

So: sort by right edge, shoot at the first balloon's end, skip everything that arrow already pops, and repeat with the first balloon left over.

## Set-up

- `points.sort(key=lambda p: p[1])` orders balloons by right edge. This is the order that makes "the balloon that ends first" always the next one we look at.
- `arrows` counts arrows fired so far.
- `arrow_x` is the position of the latest arrow, or `None` before any shot. Invariant: every balloon seen so far is popped by one of the arrows fired.

```text
sorted by end:   [1,6]  [2,8]  [7,12]  [10,16]

  0   2   4   6   8   10  12  14  16
    [1───────6]
      [2─────────8]
                [7──────12]
                      [10───────16]

arrows = 0, arrow_x = None
```

## Step by step

For each `(start, end)` in order: if `arrow_x is None or start > arrow_x`, the balloon is out of reach, so fire a new arrow at its `end`.

```text
[1,6]    arrow_x is None          -> new arrow at 6    arrows=1
[2,8]    start 2 > 6? no          -> already popped    arrows=1
[7,12]   start 7 > 6? yes         -> new arrow at 12   arrows=2
[10,16]  start 10 > 12? no        -> already popped    arrows=2

  0   2   4   6   8   10  12  14  16
    [1───────6]
      [2─────────8]
                [7──────12]
                      [10───────16]
              ^           ^
           arrow 1     arrow 2
```

The answer is `2`.

## Why it works

Take the balloon with the smallest end. Any valid plan must put an arrow inside it. Move that arrow to the balloon's end: every balloon it used to pop starts at or before that end (it overlapped this balloon) and ends no earlier (this one ends first), so it still pops them. Fixing that arrow and removing the balloons it pops leaves the same problem, smaller. Because the list is sorted by end, the next un-popped balloon is again the one with the smallest end.

## Where it goes wrong

- Sorting by start instead of end. `[1,10] [2,3] [4,5] [6,7]` is already sorted by start. The first arrow would go at 10, and the small balloons all start before 10, so they look popped: one arrow, which is wrong. Sorted by end, the arrows land at 3, 5 and 7: three arrows, which is right.
- Using `>=` instead of `>`. Balloons that only touch, like `[1,2]` and `[2,3]`, share the point 2, so one arrow at 2 pops both. The test is `start > arrow_x`, strict.
- Subtracting values to compare can overflow in languages with 32-bit integers; comparing does not.

```text
[1,2] [2,3]    arrow_x = 2,  start = 2
  start > arrow_x ?  2 > 2  false -> same arrow   (answer 1)
  with >=:           2 >= 2 true  -> extra arrow  (answer 2, wrong)
```

## Cost

Time O(n log n) for the sort; the scan is O(n). Space O(1) beyond the sort.

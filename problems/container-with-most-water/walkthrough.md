## The idea

Two walls and the floor between them hold water. The water level is set by the shorter wall, and the width is the gap between them. Checking every pair of walls works but costs O(n^2).

The shortcut is to start with the widest container and only ever give something up when it is worth it. Moving a wall inward always shrinks the width, so the only way to do better is to find a taller wall. The shorter wall is the one holding the container back, so that is the one to drop.

## Set-up

- `left` and `right` are the two walls under consideration. They start at the two ends, which is the widest possible container.
- `best` is the largest area seen so far. It starts at 0.

Invariant: every container that uses a wall outside `[left, right]` has already been measured or proven no better than something that was.

```text
height = [3, 1, 4, 2, 5]
index      0  1  2  3  4
           ▲              ▲
          left          right
```

## Step by step

Each round measures `min(height[left], height[right]) * (right - left)`, then moves the shorter side inward.

```text
Round 1  left=0 (3), right=4 (5)   area = 3 * 4 = 12   best = 12
         3 < 5, so left moves.

          ▲ left          ▲ right
         [3  1  4  2  5]

Round 2  left=1 (1), right=4 (5)   area = 1 * 3 = 3    best = 12
         1 < 5, so left moves.

Round 3  left=2 (4), right=4 (5)   area = 4 * 2 = 8    best = 12
         4 < 5, so left moves.

Round 4  left=3 (2), right=4 (5)   area = 2 * 1 = 2    best = 12
         2 < 5, so left moves. Now left == right and the loop ends.
```

The answer is 12, the very first container.

## Why it works

Take the shorter wall, say `left`. Any other container that still uses `left` has a partner no further out than `right`, so it is narrower, and it is capped by `height[left]` anyway. It cannot beat the container we just measured. So `left` has no future, and dropping it loses nothing. Each round removes one wall that can never be part of a better answer.

When the walls are equal, dropping either is fine: the code drops `right`.

## Where it goes wrong

Moving the taller wall is the tempting mistake. The cap stays at the shorter height while the width shrinks, so the area can only get worse.

```text
[3 .. 5]  area 12.  Move the 5 inward:  [3 .. x]  height <= 3, width 3
                                        area <= 9, never better
```

Also remember the area uses the gap `right - left`, not the number of walls.

## Cost

Time O(n): the two pointers together walk the array once. Space O(1): two indices and `best`.

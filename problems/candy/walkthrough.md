## The idea

Each child needs at least one candy, and a child rated higher than a neighbour must get more than that neighbour. Trying to satisfy both sides at once is awkward. Instead, split the rule in two. "Higher than my left neighbour" only looks leftward, and "higher than my right neighbour" only looks rightward. Handle each direction in its own sweep, then give each child whichever of the two requirements is bigger.

The giveaway that this works: each pass hands out the least candy its own rule permits, and the larger of two minimums satisfies both rules.

## Set-up

- `candies` starts as `[1] * n`. Everyone gets one to begin with.
- Pass one sets a floor from the left side, pass two from the right.
- Equal ratings impose no constraint on each other, so a tie never adds candy.

```text
ratings = [1, 3, 2, 2, 1]
index:      0  1  2  3  4
candies = [ 1, 1, 1, 1, 1 ]
```

## Step by step

Left to right: if `ratings[i] > ratings[i - 1]`, then `candies[i] = candies[i - 1] + 1`.

```text
i=1  3 > 1   candies[1] = 2
i=2  2 > 3?  no
i=3  2 > 2?  no  (tie)
i=4  1 > 2?  no

candies = [1, 2, 1, 1, 1]
```

Right to left: if `ratings[i] > ratings[i + 1]`, then `candies[i] = max(candies[i], candies[i + 1] + 1)`.

```text
i=3  2 > 1   max(1, 1 + 1) = 2     candies = [1, 2, 1, 2, 1]
i=2  2 > 2?  no  (tie)
i=1  3 > 2   max(2, 1 + 1) = 2     stays 2
i=0  1 > 3?  no

candies = [1, 2, 1, 2, 1]        sum = 7
```

As a picture of the two slopes:

```text
rating:   1   3   2   2   1
          ▲ up   ▼    =   ▼
candy:    1   2   1   2   1
```

## Why it works

After the left pass, every child who is rated above the left neighbour has strictly more than that neighbour, and every candy count is as small as that rule alone allows. The right pass raises counts only when the right-hand rule demands it, and the `max` keeps the left-hand guarantee intact. So both rules hold at the end. No count can be lowered without breaking one of the two rules, so the total is minimal.

At a peak the child has two slopes. The `max` makes the peak at least one above the taller of its two sides.

## Where it goes wrong

- Overwriting instead of taking the max in the second pass. A peak like the `3` in `[1, 2, 3, 1]` would lose its left climb (see below).
- Treating equal ratings as needing more candy. In `[1, 2, 2]` the last child may drop back to 1, total 4.
- Forgetting the first pass has no neighbour for `i = 0`, and the second none for `i = n - 1`; the loop ranges start at 1 and `n - 2` for that reason.

```text
Overwrite instead of max, ratings [1, 2, 3, 1]
after left pass:   [1, 2, 3, 1]
right pass i=2:    3 > 1  -> set to 2 (should be max(3, 2) = 3)
                   [1, 2, 2, 1]  and now child 2 is not above child 1
```

## Cost

Time O(n): two linear passes plus a sum. Space O(n) for `candies`.

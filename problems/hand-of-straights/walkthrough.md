## The idea

The smallest card in the hand has nothing below it to extend downwards, so it must start a group. That group is forced: it is that card plus the next `groupSize - 1` consecutive values. Remove it and repeat with the smallest card that remains.

So the answer comes from a greedy: repeatedly take the smallest remaining value and build a run upward from it, failing if some value in the run is missing. No guessing, no backtracking.

## Set-up

- First check `len(hand) % groupSize`. Every card ends up in exactly one group, so the total must divide evenly.
- `count` is a `Counter` of how many copies of each value remain.
- We walk `sorted(count)`, so we always visit the smallest value first.

```text
hand = [1, 2, 3, 6, 2, 3, 4, 7, 8]   groupSize = 3

value:  1  2  3  4  6  7  8
count:  1  2  2  1  1  1  1
```

## Step by step

At each value `card`, `need = count[card]` is how many runs must begin here. If copies are left, every one of them is a starting card, so we subtract `need` from the whole run `card .. card+groupSize-1` at once.

```text
card 1: need 1, run 1,2,3
  value:  1  2  3  4  6  7  8
  count:  0  1  1  1  1  1  1

card 2: need 1, run 2,3,4
  value:  1  2  3  4  6  7  8
  count:  0  0  0  0  1  1  1

card 3: need 0 -> skip       card 4: need 0 -> skip

card 6: need 1, run 6,7,8
  value:  1  2  3  4  6  7  8
  count:  0  0  0  0  0  0  0
```

Everything reached zero without a shortfall, so the answer is `True`.

## Why it works

Each time we reach a value with copies left, no smaller card remains, so those copies can only be group starters. Their groups are fully determined. Removing them leaves the same kind of problem, only smaller. If any value in a run has fewer copies than `need`, no valid split exists, because those starters have nowhere to go.

## Where it goes wrong

Treating duplicates as if one copy were enough. When a starter has several copies, every following value in the run needs at least that many copies too.

```text
hand = [1, 1, 2, 3]   groupSize = 2
card 1: need 2, run 1,2
  value 1: count 2 >= 2 ok -> 0
  value 2: count 1 <  2 -> return False
```

Values whose `count` is already 0 were used up by earlier runs, so the loop skips them.

## Cost

Time O(n log n): sorting the distinct values, then each value touches `groupSize` counts at most once per distinct start, so O(n) after that. Space O(n) for the `Counter`.

## The idea

Merging two triplets takes the maximum in each position, so values only go up. That one fact settles the whole problem.

If a triplet has any coordinate larger than the target's, using it in any merge pushes that coordinate above the target for good. Such a triplet can never be part of the answer. Throw it away.

Every remaining triplet is safe: all its coordinates are at most the target's. Merging all the safe ones together can never overshoot. So the only question left is whether the safe triplets, between them, reach the target value exactly in each of the three positions. No search over merge orders is needed.

## Set-up

- `found` is three booleans, one per target coordinate. `found[i]` becomes `True` once some safe triplet has exactly `target[i]` in position `i`.

```text
target = [2, 7, 5]
found  = [F, F, F]
```

## Step by step

Use `triplets = [[2,5,3], [1,8,4], [1,7,5]]` and `target = [2,7,5]`.

```text
triplet [2,5,3]   2<=2, 5<=7, 3<=5  safe
                  pos 0: 2 == 2  -> found = [T, F, F]
                  pos 1: 5 != 7, pos 2: 3 != 5

triplet [1,8,4]   8 > 7  -> skip (discarded, ignore its 4 too)
                  found = [T, F, F]

triplet [1,7,5]   1<=2, 7<=7, 5<=5  safe
                  pos 1: 7 == 7  -> found = [T, T, F]
                  pos 2: 5 == 5  -> found = [T, T, T]
```

All three are `True`, so the answer is `True`. Merging the first and third gives `[2, 7, 5]`.

## Why it works

Safe triplets merged together have a maximum in each position that is at most the target, and at least the matching value that some safe triplet supplies. If each position has a supplier equal to the target, the maximum is exactly the target. If a position has no supplier, nothing safe can ever lift that coordinate to the target, and unsafe ones overshoot, so the target is out of reach.

## Where it goes wrong

Counting a match from a discarded triplet. The check for a match must sit after the skip.

```text
triplets [[2,5,1], [1,1,1]]   target [2,1,1]
[2,5,1]: 5 > 1 -> unsafe, but it has a 2 in position 0.
If we count that 2, found[0] = T, and we answer True. Wrong.
Merging it would make the middle value 5, which is too big.
```

## Cost

Time O(n): each triplet is checked once, with three comparisons. Space O(1): the three flags.

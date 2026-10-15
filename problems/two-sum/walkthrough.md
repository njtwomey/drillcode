## The idea

The brute force tries every pair of numbers: O(n²). The improvement comes from asking a different question. Instead of "which pair adds up to `target`?", ask, for each number, "has the number I would need already appeared?". The needed number is `target - num`, its complement. A hash map answers that in constant time on average.

So one pass is enough. For each element, look for its complement among the elements before it. If it is there, we have the pair. If not, remember this element for later ones.

## Set-up

- `seen` maps a value to the index where it was found. It only contains elements strictly before the current one.

That is the invariant: when we are at index `i`, `seen` describes `nums[0..i-1]` and nothing else.

```text
nums = [2, 11, 7, 15]     target = 9

seen = {}                 i = 0, about to look at 2
```

## Step by step

```text
i=0  num=2    need 9-2 = 7     7 not in seen
              seen = {2:0}

i=1  num=11   need 9-11 = -2   -2 not in seen
              seen = {2:0, 11:1}

i=2  num=7    need 9-7 = 2     2 IS in seen, at index 0
              return [seen[2], i] = [0, 2]
```

The earlier index comes first in the answer because it was stored earlier.

## Why it works

Any valid pair has a later element and an earlier one. When the loop reaches the later one, the earlier one is already in `seen`, so the complement lookup succeeds. Since the loop stops on the first success, the answer it returns is a real pair.

## Where it goes wrong

The order of the two statements in the loop matters: check first, insert second. If you inserted `num` first, an element could find itself as its own complement.

```text
nums = [3, 2, 4]   target = 6

Insert first:   i=0  seen = {3:0}, need 3, found 3 at index 0
                returns [0, 0]   <- one element used twice

Check first:    i=0  need 3, seen empty, so insert {3:0}
                i=1  need 4, no.   i=2  need 2, found at 1
                returns [1, 2]
```

Check-first still handles duplicates: for `[3, 3]` with target 6, the first 3 is stored, and the second finds it.

## Cost

Time O(n): one pass, each lookup and insert is O(1) on average. Space O(n): in the worst case `seen` holds nearly every element before the answer is found.

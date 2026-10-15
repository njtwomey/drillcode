## The idea

A duplicate means some value appears twice. Comparing every pair is O(n^2). Instead, remember what you have already met: the first time you see a value that is already remembered, you are done. A set answers "have I seen this?" in constant time on average, so one pass is enough.

## Set-up

- `seen` is an empty set of the values passed over so far.

Invariant: at the top of each iteration, `seen` holds exactly the values from the elements before the current one, and none of them was repeated (otherwise we would already have returned).

## Step by step

Using `[4, 1, 7, 1]`:

```text
nums:   4   1   7   1
        ^
        num

num = 4   4 in seen? no     seen = {4}
num = 1   1 in seen? no     seen = {4, 1}
num = 7   7 in seen? no     seen = {4, 1, 7}
num = 1   1 in seen? YES    return True
```

If the last value were `5`, the loop would finish with `seen = {4, 1, 7, 5}` and return `False`.

## Why it works

If two equal values exist, the later one is met after the earlier one is already in `seen`, so the check fires on it. If all values are distinct, the check never fires. Empty and single-element inputs never repeat, so they fall through to `False`.

## Where it goes wrong

Add to the set only after the check, as the code does. If you add first and then test, every value finds itself and the answer is always `True`:

```text
seen.add(4); 4 in seen -> True    (it found itself)
```

## Other approaches

`containsDuplicateSorted` sorts first. Equal values then sit side by side, so only neighbours need comparing:

```text
nums    [4, 1, 7, 1]
sorted  [1, 1, 4, 7]
         ^--^ equal neighbours -> True
```

That costs O(n log n) time but needs no hash set, which is attractive when memory is tight (the sort here copies the list, so strictly in place sorting would be needed for O(1) extra space).

## Cost

The set version is O(n) time on average and O(n) space for the worst case with no duplicates. The sorted version is O(n log n) time.

## The idea

Taking the AND of every number from `left` to `right` one by one is far too slow when the range is huge. Look at what counting does to the bits instead.

As you count up from `left` to `right`, the lowest bits keep cycling through 0 and 1. If `left` and `right` differ somewhere, then at their highest differing bit, the numbers in between pass through a point where that bit flips, and everything below it resets to zeros and runs through ones. So every bit at or below that position is 0 in at least one number of the range, and the AND kills it. Only the bits above, the common binary prefix of `left` and `right`, survive.

So the answer is the common prefix, padded with zeros.

## Set-up

- `left` and `right` are shifted right together, discarding their low bits.
- `shift` counts how many times we shifted, so we know how many zero bits to put back.

Invariant: the pair `(left, right)` still has the same common prefix as the original, just shifted down by `shift` places.

```text
left = 5 = 101
right = 7 = 111

shift = 0
```

## Step by step

Shift both right until they are equal:

```text
round 0   left = 101    right = 111     differ, shift both
round 1   left =  10    right =  11     differ, shift both     shift = 1
round 2   left =   1    right =   1     equal, stop            shift = 2

answer = left << shift = 1 << 2 = 100 = 4
```

Check by hand: `5 & 6 & 7`:

```text
101
110
111
---
100   = 4
```

Another example with a longer range, 12 to 15:

```text
12 = 1100
13 = 1101
14 = 1110
15 = 1111
     ----
     1100   = 12   (prefix 11, then two zero bits)
```

## Why it works

Two numbers stop differing exactly when all their low bits have been shifted out and only the shared prefix is left. Everything shifted away lay below the highest differing bit, so it was zeroed by the AND. Shifting the prefix back left restores it to its original position with zeros underneath.

## Where it goes wrong

If `left == right`, the loop never runs and the answer is `left << 0 = left`, which is correct.

Forgetting to shift back returns just the prefix (1 instead of 4 above).

```text
5 and 7 stop at 1, not 100: you still need  1 << 2  to get 4.
```

A range that starts at 0 has prefix 0 once the numbers are shifted far enough, so the answer is 0.

## Cost

Time O(log max(right)): at most about 31 shifts for a 32-bit input. Space O(1).

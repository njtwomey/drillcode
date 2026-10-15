## The idea

Each boat carries at most two people, and their combined weight must not exceed `limit`. To use as few boats as possible, pair people up wherever you can.

Think about the heaviest person left. They need a boat no matter what. Who is the best partner to put with them? The lightest person, because if the lightest cannot fit alongside, nobody can. So after sorting, look at the two ends. If the lightest and heaviest fit together, they share a boat. If not, the heaviest goes alone.

## Set-up

- `people.sort()` lines people up by weight.
- `left` is the lightest person not yet boarded; `right` is the heaviest.
- `count` is the number of boats used.

Invariant: everyone outside `[left, right]` has already boarded a boat.

```text
people = [3, 2, 2, 1]   limit = 3
sorted ->

 idx:   0   1   2   3
        1   2   2   3
        ^           ^
      left        right
```

## Step by step

Each round uses exactly one boat and always moves `right` down. It moves `left` up only when the lightest person joined.

```text
Round 1   1 + 3 = 4 > 3   lightest does not fit, heaviest goes alone
          right -> 2, count = 1

 idx:   0   1   2   3
        1   2   2   3
        ^       ^
      left    right

Round 2   1 + 2 = 3 <= 3  they share a boat
          left -> 1, right -> 1, count = 2

 idx:   0   1   2   3
        1   2   2   3
            ^
        left=right

Round 3   2 + 2 = 4 > 3. Here left and right are the same person, so the
          sum is meaningless, but the outcome is right either way: one
          person, one boat.
          right -> 0, count = 3

left (1) > right (0): stop.   answer = 3
```

When `left == right` there is only one person left. The code adds their weight to itself, and whether or not that fits, `right` moves down and the person is counted as one boat. (If it fits, `left` also moves up, which only makes `left > right` sooner.)

## Why it works

Swapping argument: the heaviest person must board some boat. If a pairing exists at all for them, the lightest person is at least as good a partner as any other, so pairing with the lightest never costs a boat. If the lightest cannot fit with them, nobody can, so a solo boat is forced.

## Where it goes wrong

The loop condition must be `left <= right`, not `left < right`. With `<`, a final lone person (when `left == right`) is never counted.

```text
people = [5], limit = 5:   left = 0, right = 0
  with `<`:   loop never runs, count = 0   wrong
  with `<=`:  loop runs once, count = 1    right
```

Counting a boat per pair instead of per round also goes wrong when someone travels alone.

## Cost

Time O(n log n) for the sort; the two-pointer pass is O(n). Space O(1) beyond the sort.

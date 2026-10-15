## The idea

Now the last index is always reachable, and we want the fewest jumps. Think of it as a breadth-first search where the "levels" are ranges of indices: everything reachable in 1 jump, then everything reachable in 2, and so on. Because reachable indices form a block, each level is just a range, so we never need a queue.

To go from one level to the next you only care about the farthest index anyone in the current level can reach. The jump count rises exactly when we finish scanning a level.

## Set-up

- `jumps` is the number of jumps taken so far. It starts at 0.
- `end` is the last index reachable with `jumps` jumps. It starts at 0, because with no jumps you are at index 0.
- `farthest` is the last index reachable with `jumps + 1` jumps, found by scanning the current level.
- The loop runs over `range(len(nums) - 1)`: no jump is needed from the last index.

```text
nums = [2, 3, 1, 1, 4]

 index:   0  1  2  3  4
 value:   2  3  1  1  4
 jumps=0  end=0  farthest=0
```

## Step by step

```text
i=0  farthest = max(0, 0+2) = 2
     i == end (0): level 0 done. jumps = 1, end = 2.
     level 1 is indices 1..2

i=1  farthest = max(2, 1+3) = 4
i=2  farthest = max(4, 2+1) = 4
     i == end (2): level 1 done. jumps = 2, end = 4.
     level 2 is indices 3..4 and includes the last index

i=3  farthest = max(4, 3+1) = 4
     i != end (4)
loop stops before i=4
return jumps = 2
```

```text
index:  0 | 1  2 | 3  4
level:  0 |  1   |  2
        jump 1: 0 -> {1,2}     jump 2: 1 -> 4
```

## Why it works

Anything reachable in `k` jumps is reachable from some index in level `k-1`. Among the indices of a level, the one that reaches farthest dominates the others: any route that uses a different index can swap to this one and still land on whatever it would have, since landing spots form a block. So the next level is just `(end, farthest]`, and counting levels counts jumps.

## Where it goes wrong

- Looping to the last index. At `i == n-1` with `i == end` we would count one extra jump that no one needs. For `[1, 2]` the first jump already ends at the last index; the loop only visits index 0.
- A single element `[0]` makes `range(0)` empty, so the answer is 0, which is right.
- Incrementing `jumps` on every index rather than only when `i == end` counts steps instead of levels.

## Cost

Time O(n): one pass. Space O(1): three integers.

## The idea

For every cell we want the distance to the nearest 0. The obvious plan is to start a search from each 1 and look for the closest 0, but that repeats a lot of work.

Turn it around. Start from all the zeros at once and spread outward one step at a time, like ripples from several stones dropped in a pond at the same moment. A cell gets its distance the first time any ripple reaches it, and because the ripples expand at the same speed, the first ripple to arrive is the one from the nearest zero. This is a breadth-first search (BFS) with many sources.

## Set-up

- `result` is a grid the same size as `mat`, filled with `-1`. `-1` means "distance not found yet", so the grid doubles as the visited set.
- `queue` holds cells whose distance is known and whose neighbours have not been looked at yet. It starts with every 0, each recorded with distance 0.

Invariant: the queue holds cells in non-decreasing order of distance, so cells at distance `d` all come out before any at `d + 1`.

```text
mat           result (initial)        queue
0 0 0         0  0  0                 (0,0) (0,1) (0,2) (1,0) (1,2)
0 1 0         0 -1  0
1 1 1        -1 -1 -1
```

## Step by step

Popping a cell, we look at its four neighbours. Any neighbour still at `-1` gets `result[r][c] + 1` and joins the queue.

```text
Pop the zeros in order. (0,0) and (0,2) find nothing new.

Pop (0,1): neighbour (1,1) is -1 -> set to 1, push.
Pop (1,0): neighbour (2,0) is -1 -> set to 1, push.
Pop (1,2): neighbour (2,2) is -1 -> set to 1, push.

   0  0  0
   0  1  0           queue now: (1,1) (2,0) (2,2)
   1 -1  1
```

```text
Pop (1,1) at distance 1: neighbour (2,1) is -1 -> set to 2, push.
Pop (2,0), (2,2): all their neighbours are already filled.
Pop (2,1): nothing left to fill.

   0  0  0
   0  1  0           final answer
   1  2  1
```

## Why it works

BFS processes cells in order of distance. A cell is first discovered by the earliest ripple to touch it, and no later ripple can have a shorter path. Seeding with all zeros together means "distance from the nearest zero" is exactly "number of rounds until discovered".

## Where it goes wrong

Searching from each 1 separately is correct but costs O((m * n)²) in the worst case. Another trap is updating a cell twice: the `== -1` test prevents that, so every cell is enqueued once. If you forgot to mark zeros as `0` up front, the neighbours would write over them.

## Cost

Time O(m * n): each cell enters the queue once and checks four neighbours. Space O(m * n) for `result` and the queue.

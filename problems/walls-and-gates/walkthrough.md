## The idea

The slow way is to start from each empty room and search for the nearest gate. That repeats a lot of work. Reverse the viewpoint: start from all the gates at once and spread outward. Because the spread moves one step per round for every gate at the same time, the first time any room is reached is from its nearest gate, at the smallest distance.

That is a breadth-first search with many sources. One pass over the grid labels every room.

## Set-up

- `INF` is the value of an empty room that has not been reached.
- `queue` is a deque seeded with every gate cell `(r, c)` where the room is 0. Invariant: the queue is ordered by distance, so cells at distance `d` come before cells at distance `d + 1`.
- The grid is its own visited set. A neighbour is only taken if it is still `INF`. Walls (-1) and rooms already labelled are skipped.

Below, `.` is `INF` and `#` is a wall.

```text
 col  0  1  2  3
 r0   .  #  0  .
 r1   .  .  .  #
 r2   .  #  .  #
 r3   0  #  .  .

 queue = [(0,2), (3,0)]
```

## Step by step

Each pop writes `rooms[r][c] + 1` into the INF neighbours and enqueues them. Here is the grid after each wave of the queue finishes.

```text
after distance 1      after distance 2      after distance 3
 .  #  0  1            .  #  0  1            3  #  0  1
 .  .  1  #            2  2  1  #            2  2  1  #
 1  #  .  #            1  #  2  #            1  #  2  #
 0  #  .  .            0  #  .  .            0  #  3  .

after distance 4 (final)
 3  #  0  1
 2  2  1  #
 1  #  2  #
 0  #  3  4
```

The gate at `(0,2)` reaches `(0,3)` and `(1,2)` first. The gate at `(3,0)` reaches `(2,0)` and then climbs up the left column. The room at `(1,1)` is reached from `(1,2)`, so it gets 2.

## Why it works

BFS visits cells in order of distance from the nearest source, because the queue holds all cells at distance `d` before any at `d + 1`. The first write into a room is therefore its shortest distance, and that write turns it from INF into a number so it is never written again. A room no gate can reach is never enqueued and stays INF.

## Where it goes wrong

Checking `rooms[nr][nc] == INF` is the whole visited test. If you let the search enter any non-wall cell, it would go back to gates and already-labelled rooms and overwrite correct distances.

```text
no INF check: (1,2) = 1 spreads to (0,2) the gate, writing 2 over a 0
```

Also note that no gates means the queue starts empty and everything stays INF, and a one-cell grid is handled by the same loop.

## Cost

Each cell is enqueued at most once and has four neighbours, so time is O(m * n). Space is O(m * n) for the queue in the worst case.

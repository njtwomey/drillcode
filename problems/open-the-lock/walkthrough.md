## The idea

Think of each of the 10,000 wheel positions (`"0000"` to `"9999"`) as a node. One turn of one wheel is an edge, so every node has 8 neighbours: 4 wheels, each up or down. The question is the fewest turns from `"0000"` to `target` without touching a dead end. Fewest steps in an unweighted graph means breadth-first search.

Dead ends are not special logic: they are nodes we mark as already visited, so BFS never enters them.

## Set-up

- `seen = set(deadends)`, then `"0000"` added. If `"0000"` was a dead end the lock is jammed at the start, so return `-1` right away.
- `queue` holds `(state, turns)` pairs, starting with `("0000", 0)`.
- Invariant: states leave the queue in order of non-decreasing `turns`, so the first time `target` comes out, it has the fewest turns.
- A state goes into `seen` when it is queued, so it is never queued twice.

```text
deadends = ["8888"]    target = "0009"

seen  = {"8888", "0000"}
queue = [("0000", 0)]
```

## Step by step

Pop a state; if it is `target`, return its turns. Otherwise build the 8 neighbours by changing one digit by `+1` or `-1` modulo 10 (so `0 - 1` becomes `9`), and queue the unseen ones with `turns + 1`.

```text
pop ("0000", 0)   not the target. Neighbours, in code order:
    wheel 0:  1000   9000
    wheel 1:  0100   0900
    wheel 2:  0010   0090
    wheel 3:  0001   0009
  queue = [1000 9000 0100 0900 0010 0090 0001 0009]   all at turns = 1

pop 1000, 9000, 0100, 0900, 0010, 0090, 0001   none is the target
  (each one queues its own 7 new neighbours at turns = 2)

pop ("0009", 1)   equals target -> return 1
```

The last wheel went from 0 down to 9 in one turn because of the wrap, so the answer is `1`.

A dead end changes the route. With `deadends = ["0001"]` and `target = "0002"` the direct path is blocked, so BFS finds a detour:

```text
0000 ──▶ 0010 ──▶ 0011 ──▶ 0012 ──▶ 0002
  0       1        2         3        4   turns
  (0001 is never entered)
```

## Why it works

BFS visits every state at distance 1, then every state at distance 2, and so on. The first time it sees `target` is therefore along a shortest path that avoids the blocked nodes. Marking states seen when queued keeps the work to at most 10,000 states, each tried with 8 moves.

## Where it goes wrong

- Forgetting the `"0000"` dead-end check. Starting from a jammed lock must give `-1`, even if `target` is `"0000"`.
- Forgetting the wrap. `(digit - 1) % 10` is `9` for a `0` wheel in Python, which is what is wanted; using `digit - 1` would produce `-1` in the string.
- Putting dead ends into `seen` only after popping, which lets BFS walk into them first.

```text
digit 0, step -1:  (0 - 1) % 10 = 9    -> "0009" is one turn away from "0000"
digit 9, step +1:  (9 + 1) % 10 = 0    -> "9" wraps back to "0"
```

## Cost

Time O(10^4 * 8): each of the 10,000 states is expanded once with 8 neighbours. Space O(10^4) for `seen` and the queue.

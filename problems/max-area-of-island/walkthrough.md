## The idea

An island is a group of land cells joined up, down, left or right. Scan the grid. The first time you meet an unvisited land cell, you have found a new island, so flood outward from it, count the cells you reach, and compare with the best so far. The flood must mark cells so none is counted twice.

The marking trick: overwrite each land cell with `0` as soon as it is visited, so the grid doubles as the visited set.

## Set-up

- `best` is the largest area seen.
- `area` is the count for the island being flooded.
- `stack` holds cells waiting to be explored. A stack (not recursion) avoids the recursion limit when a single island fills a big grid.
- Invariant: a cell is set to `0` at the moment it is pushed, so it can be on the stack at most once.

## Step by step

```text
grid                  
 1 1 0 0
 0 1 0 1
 0 0 0 1
 1 0 0 0
```

The scan reaches `(0,0)`. Sink it, `stack = [(0,0)]`.

```text
pop (0,0)  area 1   push (0,1)                    stack [(0,1)]
pop (0,1)  area 2   push (1,1)                    stack [(1,1)]
pop (1,1)  area 3   no land neighbours left       stack []
```

The island has area 3 and `best = 3`. The grid now:

```text
 0 0 0 0
 0 0 0 1
 0 0 0 1
 1 0 0 0
```

The scan next reaches `(1,3)`:

```text
pop (1,3)  area 1   push (2,3)
pop (2,3)  area 2   nothing new                   area 2, best stays 3
```

Then `(3,0)` floods a single cell for area 1. The answer is 3. The cells `(1,3)` and `(3,0)` are never reached by the first flood because nothing links them. Diagonal neighbours are not checked, so diagonal land would be a separate island.

## Why it works

The flood from a cell visits exactly the cells reachable through land neighbours, which is the definition of an island. Sinking cells ensures each is counted once, and the outer scan ensures every island gets flooded once, since a sunk cell is never a starting point again.

## Where it goes wrong

Marking cells when you pop them, instead of when you push them, lets the same cell be pushed by two neighbours before either is popped, and then it is counted twice:

```text
 1 1        pop (0,1), push (1,1)
 1 1        pop (1,1), (1,0) still 1 and still on the stack: pushed again
 area comes out 5 for a 4-cell island
```

## Cost

Time O(m * n): every cell is looked at a constant number of times. Space O(m * n) for the stack in the worst case. The grid is modified in place, so copy it first if the caller needs it.

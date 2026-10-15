## The idea

To find a word in a grid by moving to neighbouring cells, you have to try routes. There is no shortcut around that, but you can make each route cheap. Start at any cell whose letter matches the first letter. From there, look at the four neighbours for the next letter. Whenever a neighbour does not match, abandon that direction immediately. This is depth-first search with backtracking.

The twist is that a path may not use the same cell twice. So the cell you are standing on has to count as unavailable for everything deeper in this route, but available again once you back out of it, because a different route may want it.

## Set-up

- `dfs(r, c, i)` answers: can `word[i:]` be matched starting at cell `(r, c)`?
- Base case: `i == len(word)` means every letter has been matched, so return True.
- Failure: the cell is off the grid, or its letter is not `word[i]`.
- Instead of a visited set, the code overwrites the current cell with `"#"` while exploring, and puts the letter back afterwards. A `"#"` never equals a letter, so the match test rejects it for free.
- A quick prune up front: if the word is longer than the number of cells, return False.

```text
board                word = "ABCCED"
   c: 0  1  2  3
r=0   A  B  C  E
r=1   S  F  C  S
r=2   A  D  E  E
```

## Step by step

The neighbours are tried in the order down, up, right, left. The outer `any(...)` tries start cells row by row, so the first start is `(0,0)`.

```text
dfs(0,0,0)  'A' == word[0]     mark (0,0).  down (1,0) is 'S' != 'B': fail
dfs(0,1,1)  'B' == word[1]     mark (0,1).  down (1,1) 'F' != 'C': fail
                                            up: off grid
dfs(0,2,2)  'C' == word[2]     mark (0,2).  down is next
dfs(1,2,3)  'C' == word[3]     mark (1,2).
dfs(2,2,4)  'E' == word[4]     mark (2,2).  down: off. up: (1,2) is '#': fail
                                            right (2,3) 'E' != 'D': fail
                                            left is next
dfs(2,1,5)  'D' == word[5]     mark (2,1)
dfs(?,?,6)  i == len(word)     True
```

The grid while the deepest call runs, with `#` on the current path:

```text
   A  B  C  E          #  #  #  E
   S  F  C  S    ->    S  F  #  S
   A  D  E  E          A  #  #  E
```

As each call returns True, `found` is True, the cell is restored, and True propagates up. When a call returns False the restore still runs, so the board always ends up as it began.

## Why it works

Every route is either extended one valid letter at a time or cut off at the first mismatch, so all legal paths are explored and nothing else. The `"#"` mark is applied before recursing and removed after, so it is present for exactly the cells on the current path. The `or` chain stops at the first success.

## Where it goes wrong

- Forgetting to restore the cell. A failed branch would leave `"#"` behind and block later routes. On `[["a","a"]]` with `"aaa"` this is harmless, but on larger boards it makes valid words disappear.
- Checking the letter before the bounds. `board[-1][c]` wraps around in Python instead of failing, so the bounds test must come first.
- Reusing a cell, as in the `"ABCB"` example: the second `B` is the cell already on the path, which is now `"#"`.

## Cost

Time O(m·n·3^L) for an m by n grid and word length L: each start cell can branch into at most three new directions per step, since the cell it came from is marked. Space O(L) for the recursion depth; the marking is done in place.

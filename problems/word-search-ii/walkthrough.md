## The idea

Searching for one word is a standard grid DFS. Doing it separately for up to 30,000 words repeats the same walks again and again, especially for words that share a prefix.

Put every word in a trie (a tree of letters). Then run one DFS from each cell, following only letters that are children of the current trie node. A path that matches no word's prefix is abandoned immediately, and every word along the way is found in the same walk.

## Set-up

- `root` is the trie, built from nested dicts. Each key is a letter. The key `"$"` marks the end of a word and stores the word itself.
- `result` collects the found words.
- `dfs(r, c, parent)` assumes `board[r][c]` is a child of `parent`. It moves into `node = parent[ch]`.
- Marking a cell `"#"` while on the current path stops reuse; `"#"` is never a trie key.

Small example: board `[["o","a"],["e","t"]]`, words `oat`, `oak`, `ate`.

```text
board          trie
 o a            root
 e t            ├─ o ── a ──┬─ t ── $ "oat"
                │           └─ k ── $ "oak"
                └─ a ── t ── e ── $ "ate"
```

## Step by step

```text
start (0,0) 'o' is a root child.
  mark (0,0) '#'. Neighbours: (1,0) 'e' not under o; (0,1) 'a' is.
  (0,1) 'a': node o.a, mark '#'. Neighbours: (1,1) 't' is under o.a.
    (1,1) 't': node o.a.t has "$" -> found "oat". pop removes "$".
      node is empty now; after backtracking, delete 't' from o.a.
      trie: o ── a ── k ── $ "oak"

start (0,1) 'a' is a root child.
  (1,1) 't' is under a. Then (1,0) 'e' is under a.t.
    (1,0) 'e': found "ate".  Empty branches pruned all the way up:
      e deleted, then t, then a. Trie: o ── a ── k ── $ "oak"
```

"oak" is never found: no `k` is on the board, so the `k` branch is never entered. Result: `["oat", "ate"]`.

## Why it works

The trie guarantees the path so far is a prefix of some word, so every explored path can still become a word, and every word on the board is reachable as a trie path from the cell it starts at. Restoring `board[r][c] = ch` after the neighbours makes the "no reuse" rule apply per path, not globally.

## Where it goes wrong

- Reporting the same word twice when it can be spelled by several paths. `node.pop("$", None)` makes the report happen once.
- Forgetting to restore the cell after recursing, which hides the cell from every later path.
- Not pruning exhausted trie nodes. Correct, but dense boards then re-walk dead branches and slow down a lot.
- Checking the neighbour against the trie before recursing, not after, saves a call at every dead end.

## Cost

Time O(m * n * 3^L): from each cell the DFS goes at most L deep, with at most three new directions after the first. Space O(total letters in words) for the trie, plus O(L) recursion.

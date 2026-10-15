## The idea

Storing words in a list means every search checks every word. A trie shares prefixes: each word is a path from the root, one letter per edge, so looking up a word costs the length of the word, not the number of words.

The new twist is the `.` wildcard, which matches any single letter. For ordinary letters you still follow the one matching edge. For a `.` you do not know which branch is right, so try all of them with a depth-first search and succeed if any works.

## Set-up

The trie is nested dicts in `self.root`.

- Each key is a letter, and its value is the dict for the next level.
- The special key `"$"` marks that a word ends at this node. Without it, a stored `"bad"` would make the prefix `"ba"` look like a word.
- `addWord` walks down using `setdefault`, creating nodes as needed, then sets `"$"`.
- `search` uses an inner `dfs(node, i)`: can `word[i:]` be matched below this node?

After adding `bad`, `dad`, `mad`:

```text
root
├─ b ─ a ─ d ─ $
├─ d ─ a ─ d ─ $
└─ m ─ a ─ d ─ $
```

## Step by step

```text
search("pad")
  dfs(root, 0)  ch='p'  no child 'p'  ──▶ False

search("bad")
  dfs(root,0) 'b' ─▶ dfs(b,1) 'a' ─▶ dfs(a,2) 'd' ─▶ dfs(d,3)
  i == len(word): is "$" in the node?  yes  ──▶ True

search(".ad")
  dfs(root,0)  ch='.'  try each child, skipping "$"
    child b:  dfs(b,1) 'a' ─▶ dfs(a,2) 'd' ─▶ dfs(d,3)  "$" present ──▶ True
  first branch already works, stop

search(".at")
  dfs(root,0)  ch='.'
    child b:  ... 'a' ok, then 't' not a child of that node ──▶ False
    child d:  same ──▶ False
    child m:  same ──▶ False
  no branch worked ──▶ False
```

## Why it works

A path from the root spells a prefix, and `"$"` says that prefix is a complete word. `dfs(node, i)` is true exactly when some stored word matches `word[i:]` starting from this node. A plain letter has one candidate edge; a `.` has all of them, so trying every child covers every possible letter it could stand for.

## Where it goes wrong

Two traps:

- Checking `"$"` only when the node exists is not enough: reaching the end of the pattern at a node without `"$"` (a mere prefix) must return `False`. Pattern `"ba"` against the trie above fails for this reason.
- When looping over children for a `.`, skip the `"$"` key. It is a marker, not a letter, and its value is `True`, not a dict.

## Cost

`addWord` is O(L) time for a word of length L. `search` is O(L) when the pattern has no dots, and up to O(26^L) in the worst case with many dots (bounded by the size of the trie). Space is O(total characters stored).

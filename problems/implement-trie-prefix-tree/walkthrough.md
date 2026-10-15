## The idea

A trie stores words as paths. Each node stands for a prefix, and each edge adds one letter. Words that share a beginning share the nodes for that beginning, so "apple" and "app" use the same first three nodes.

Looking up a word or a prefix then costs one step per letter, no matter how many words are stored. A list of words would need a scan, and even a set of words cannot answer "does anything start with this?" without checking every entry.

## Set-up

- `_TrieNode.children` is a dict from a letter to the child node. The path from the root spells the prefix.
- `_TrieNode.is_word` is a flag meaning "a stored word ends exactly here". Without it we could not tell the word "app" from the mere prefix of "apple".
- `Trie.root` is an empty node that represents the empty prefix.
- `_walk(prefix)` follows the letters and returns the node where they end, or `None` if the path breaks. Both `search` and `startsWith` use it.

```text
root (empty)
```

## Step by step

Operations: `insert("apple")`, `search("apple")`, `search("app")`, `startsWith("app")`, `insert("app")`, `search("app")`. A `*` marks a node whose `is_word` is true.

```text
after insert("apple"):

 root ─a─▶ ─p─▶ ─p─▶ ─l─▶ ─e─▶ (*)
                              is_word set on the last node only

search("apple"): _walk reaches the e node, is_word is True     -> True
search("app"):   _walk reaches the second p node, is_word is
                 False                                         -> False
startsWith("app"): _walk reaches that node, which is not None  -> True

insert("app"): the path already exists, no new nodes; just
               set is_word on the second p node.

 root ─a─▶ ─p─▶ ─p─(*)─▶ ─l─▶ ─e─(*)

search("app"): same node as before, is_word is now True        -> True
```

The only difference between `search` and `startsWith` is the final check: `search` also requires `is_word`.

## Why it works

Every node corresponds to exactly one prefix, because the path from the root to it is unique. Following a prefix either succeeds, in which case some stored word passes through that node, or fails at the first missing letter, in which case no stored word has that prefix. The flag separates "a word ends here" from "a word merely passes through".

## Where it goes wrong

- Returning `True` from `search` as soon as the walk succeeds. That would make `search("app")` true after inserting only "apple".
- Forgetting to set `is_word` after the loop in `insert`. Inserting "app" after "apple" creates no nodes, so the flag is the only change.
- In `_walk`, using `children[ch]` instead of `.get(ch)` raises `KeyError` on a missing letter.

## Cost

Each operation takes O(L) time for a word of length L, independent of how many words are stored. Space is O(total characters) in the worst case, when no two words share a prefix; shared prefixes cost nothing extra.

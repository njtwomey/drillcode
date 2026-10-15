## The idea

A sorted list of words in an unknown alphabet hides ordering rules about the letters. Take two neighbouring words and find the first position where they differ. That pair of letters tells you something: the one in the earlier word comes before the one in the later word. Nothing after that position says anything, since the words are already ordered by that earlier difference.

Collect those rules as arrows `a -> b` ("a comes before b"). The alphabet order is then any ordering that respects every arrow, which is a topological sort. If the arrows form a loop, no order exists.

## Set-up

- `edges[c]` is the set of letters that must come after `c`. Every letter that appears in any word gets an entry, even if no rule mentions it, so it still shows up in the answer.
- `indegree[c]` counts the rules pointing into `c`, that is, how many distinct letters must come before it.
- Using a set for `edges` stops the same rule being counted twice and inflating `indegree`.

Take `["wrt", "wrf", "er", "ett", "rftt"]`. Comparing each adjacent pair:

```text
wrt  vs wrf    first difference at index 2:  t vs f   ->  t -> f
wrf  vs er     index 0:                      w vs e   ->  w -> e
er   vs ett    index 1:                      r vs t   ->  r -> t
ett  vs rftt   index 0:                      e vs r   ->  e -> r
```

```text
 w ──▶ e ──▶ r ──▶ t ──▶ f

 indegree:  w=0  r=1  t=1  f=1  e=1
```

## Step by step

Kahn's algorithm: emit any letter with `indegree` 0, then remove its outgoing arrows.

```text
queue = [w]                 result = []

pop w   result = w           e: 1 -> 0, enqueue e     queue = [e]
pop e   result = we          r: 1 -> 0, enqueue r     queue = [r]
pop r   result = wer         t: 1 -> 0, enqueue t     queue = [t]
pop t   result = wert        f: 1 -> 0, enqueue f     queue = [f]
pop f   result = wertf       no outgoing edges        queue = []
```

All 5 letters were emitted, so the answer is `"wertf"`.

## Why it works

A letter is emitted only when everything required to precede it has already been emitted, so the output satisfies every rule. If the rules contain a cycle, say `z -> x -> z`, no letter on it ever reaches indegree 0, so none is emitted and `len(result) < len(edges)`. The code detects that and returns an empty string.

## Where it goes wrong

- Reading rules from later letters. In `"wrt"` vs `"wrf"`, only `t` vs `f` counts. The `w` and `r` are equal and tell you nothing.
- Missing the prefix trap. `["abc", "ab"]` is impossible, because a prefix must come first. The loop over letters would find no difference, so the code checks this case explicitly and returns `""`.
- Only creating nodes for letters that appear in rules. `["ab", "adc"]` gives one rule, `b -> d`, but the answer must also include `a` and `c`.
- Dropping the `break` after the first difference.

## Cost

Time O(C), where C is the total number of characters across all words: one pass to build the graph and then work proportional to the number of letters and rules, which is bounded by the alphabet size. Space O(1) in terms of the alphabet (at most 26 nodes and 26 x 26 edges).

## The idea

Treat each word as a node and connect two words if they differ in exactly one letter. The shortest transformation is then the shortest path in an unweighted graph, which is what breadth-first search finds: the first time we reach `endWord`, the number of levels used is the answer.

The expensive part is finding neighbours. Comparing a word against every other word is O(N) per word. Instead, group words by wildcard pattern: `hot` belongs to `*ot`, `h*t` and `ho*`. Two words that share a pattern differ only in the wildcard position, so a pattern lookup returns neighbours directly.

## Set-up

- `words` is a set of the list; if `endWord` is not in it, return 0 at once.
- `buckets` maps each pattern to the words that fit it.
- `seen` holds words already queued, starting with `beginWord`. It need not be in the list.
- `queue` holds `(word, steps)` pairs, where `steps` counts words on the path so far, starting at 1 for `beginWord`.

```text
words: hot dot dog lot log cog       begin hit, end cog

buckets (only the ones that matter)
  *ot : hot dot lot        h*t : hot        do* : dot dog
  lo* : lot log            *og : dog log cog

queue = [(hit, 1)]     seen = {hit}
```

## Step by step

Each round pops a word, tries each of its patterns, and queues every unseen word in those buckets. Popping the bucket (rather than reading it) empties it, since all its words are queued after one visit.

```text
pop hit (1)   h*t -> hot                  queue: hot(2)
pop hot (2)   *ot -> dot, lot             queue: dot(3) lot(3)
pop dot (3)   do* -> dog                  queue: lot(3) dog(4)
pop lot (3)   lo* -> log                  queue: dog(4) log(4)
pop dog (4)   *og -> log (seen), cog      queue: log(4) cog(5)
pop log (4)   nothing new
pop cog (5)   equals endWord -> return 5
```

```text
hit ──▶ hot ──▶ dot ──▶ dog ──▶ cog       5 words
            └─▶ lot ──▶ log ──┘
```

## Why it works

BFS pops words in order of distance from `beginWord`. The first time `endWord` is popped, no shorter path can exist. Because every word sharing a pattern is one letter away, the buckets give exactly the graph edges. Emptying a bucket after its first use is safe: all its members are already in `seen`, and BFS never needs a longer route to them.

## Where it goes wrong

- Skipping the early return when `endWord` is not in the list. The search would still end with 0, but only after exploring everything reachable.
- Starting `steps` at 0 gives an answer one too small. The count includes both end words.
- Not checking `seen`: words appear in several buckets, so they would be queued repeatedly.

## Cost

Building buckets is O(N * L) patterns, each costing O(L) to build, so O(N * L²) time and space. The BFS visits each word once and each bucket once. Here N is the word count and L the word length.

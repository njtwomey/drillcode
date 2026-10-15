## The idea

Two words are anagrams when they contain the same letters the same number of times. So if we can turn each word into a "fingerprint" that only depends on its letter counts, anagrams get identical fingerprints and grouping becomes a dictionary lookup.

The brute force compares every word against every other word, which is quadratic in the number of words. With a fingerprint we touch each word once and drop it into the right bucket.

## Set-up

- `groups` is a `defaultdict(list)` from fingerprint to the words that have it. A missing key quietly becomes an empty list, so we never need an "is it there yet?" check.
- `counts` is a fresh 26-slot list per word: slot 0 counts `a`, slot 1 counts `b`, and so on.
- The fingerprint is `tuple(counts)`. Lists cannot be dictionary keys because they are mutable; a tuple can.

Counting is linear in the word's length, while sorting the letters (the other common fingerprint) costs more. Both work.

```text
groups = {}            (empty)
```

## Step by step

Input: `["eat", "tea", "tan", "ate", "nat", "bat"]`. Writing each fingerprint as its non-zero counts:

```text
word   counts                fingerprint key   groups afterwards
─────  ────────────────────  ────────────────  ─────────────────────────────
eat    a1 e1 t1              (a1 e1 t1)        {aet: [eat]}
tea    a1 e1 t1              (a1 e1 t1)        {aet: [eat, tea]}
tan    a1 n1 t1              (a1 n1 t1)        {aet: [eat, tea], ant: [tan]}
ate    a1 e1 t1              (a1 e1 t1)        {aet: [eat, tea, ate], ant: [tan]}
nat    a1 n1 t1              (a1 n1 t1)        {aet: [...3], ant: [tan, nat]}
bat    a1 b1 t1              (a1 b1 t1)        {aet: [...3], ant: [...2], abt: [bat]}
```

Here `aet`, `ant` and `abt` are just short labels for the real 26-number tuples. At the end `list(groups.values())` gives:

```text
[ [eat, tea, ate],  [tan, nat],  [bat] ]
```

## Why it works

The count tuple determines the multiset of letters exactly, and two words are anagrams precisely when those multisets are equal. So equal key means anagram, and different key means not. Every word lands in exactly one bucket.

## Where it goes wrong

- Using the list `counts` itself as the key raises `TypeError: unhashable type`. Convert it to a tuple.
- Reusing one `counts` list across words would mix their letters. It must be created inside the loop.
- The empty string is a valid word. Its key is 26 zeros, so all empty strings group together, which is correct.

## Cost

Time O(n * k) for n words of length up to k: one pass over each word's letters. Space O(n * k) for the buckets, plus a constant 26 slots for `counts`. Sorting each word instead would make the time O(n * k log k).

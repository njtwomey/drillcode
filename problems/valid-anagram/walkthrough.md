## The idea

Two strings are anagrams when they use exactly the same letters the same number of times, just in a different order. Order is irrelevant, so throw it away: all that matters is a tally of how often each letter appears. If the tallies match, the strings are anagrams.

Sorting both strings and comparing also works, but sorting costs O(n log n). Counting is a single pass over each string, O(n).

## Set-up

- A length check first. Strings of different lengths cannot have the same tallies, so return `False` without counting anything.
- `Counter(s)` and `Counter(t)` are dictionaries from character to count. They are built from the strings and compared with `==`, which is true when both have the same keys with the same counts.

```text
s = "listen"          t = "silent"

Counter(s):  l:1  i:1  s:1  t:1  e:1  n:1
Counter(t):  s:1  i:1  l:1  e:1  n:1  t:1
```

## Step by step

Counting is just walking the string and adding one to each letter's slot:

```text
 s = "aab"           a  b            t = "aba"           a  b
 read 'a'            1  0            read 'a'            1  0
 read 'a'            2  0            read 'b'            1  1
 read 'b'            2  1            read 'a'            2  1
                    -----                               -----
                    a:2 b:1                              a:2 b:1   equal -> True
```

A mismatch looks like this:

```text
 s = "rat"      r:1 a:1 t:1
 t = "car"      c:1 a:1 r:1        't' vs 'c' differ -> False
```

## Why it works

Rearranging a string never changes how many of each letter it has, and a string is fully determined, up to order, by those counts. So equal counts mean one string can be rearranged into the other, and unequal counts mean it cannot.

## Where it goes wrong

Without the length check, a plain comparison still works here, because the `Counter` equality would catch extra letters. The check is just a cheap early exit.

The trap is comparing only the sets of letters: `"aab"` and `"abb"` have the same set `{a, b}` but different counts.

```text
"aab"  a:2 b:1
"abb"  a:1 b:2     same letters, different counts -> not anagrams
```

## Cost

Time O(n): one pass over each string. Space O(1) in the sense that the alphabet is fixed (26 letters), so each counter has a bounded number of entries. For arbitrary Unicode input the space grows with the number of distinct characters.

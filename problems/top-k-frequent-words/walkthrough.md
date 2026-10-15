## The idea

This is "top k by frequency" with a twist: when two words are equally common, the alphabetically smaller one ranks first. The twist is easy to fold in. Sort-by-key lets a tuple express both rules, and since smaller tuples come first, negate the count so higher frequency sorts earlier. The key is `(-count[word], word)`: more frequent first, then alphabetical.

Then take the `k` smallest by that key. `heapq.nsmallest` does this with a bounded heap of size `k`, so it avoids a full sort of every distinct word.

## Set-up

- `count = Counter(words)` maps each distinct word to its frequency.
- The key function maps a word to `(-count[word], word)`. Tuples compare left to right, so the count decides first and the word breaks ties.
- `heapq.nsmallest(k, count, key=...)` iterates over the distinct words (the dictionary keys) and keeps only the `k` best at any time.

```text
words = ["i", "love", "leetcode", "i", "love", "coding"]    k = 2

count: i -> 2, love -> 2, leetcode -> 1, coding -> 1
```

## Step by step

Compute each word's key, then order by it.

```text
word       key
i          (-2, "i")
love       (-2, "love")
leetcode   (-1, "leetcode")
coding     (-1, "coding")

ascending order of keys:
  (-2, "i")  <  (-2, "love")  <  (-1, "coding")  <  (-1, "leetcode")
```

The two 2-count words tie on the first part, so the second part orders them: `"i" < "love"`. The two smallest keys are the answer: `["i", "love"]`.

In the larger example, counts the:4, is:3, sunny:2, day:1 give keys `(-4,"the") < (-3,"is") < (-2,"sunny") < (-1,"day")`, so `k = 4` returns `["the", "is", "sunny", "day"]`.

## Why it works

Sorting by a key is correct if the key's order matches the order we want. The tuple does that exactly: lower first element means higher frequency, and equal first elements fall through to alphabetical order. `nsmallest` returns the `k` smallest elements in sorted order, so the output is already in the order the problem asks for.

## Where it goes wrong

- Forgetting the negation. `(count, word)` ascending puts the LEAST frequent words first.

```text
(count, word):   (1,"coding") (1,"leetcode") (2,"i") ...   <- wrong end
(-count, word):  (-2,"i") (-2,"love") (-1,"coding") ...    <- right
```

- Breaking ties by insertion order instead of alphabetically. A bucket sort by count must sort within the bucket; the tuple key does this by itself.
- Passing the whole word list to `nsmallest`. Pass the `Counter` (its keys), so each distinct word is considered once.

## Cost

Time O(n + d log k) for `n` words and `d` distinct words, usually written O(n log k). Space O(d) for the counter, plus O(k) for the heap.

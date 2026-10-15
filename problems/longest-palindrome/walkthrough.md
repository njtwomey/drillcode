## The idea

You may rearrange the letters freely, so the question is not about finding a palindrome inside the string. It is about how many letters you can place symmetrically.

A palindrome is made of mirrored pairs, plus at most one letter in the middle that has no partner. So count each letter. Every full pair of a letter can be used. If any letter has a spare single left over, one such letter can be the centre, adding 1 to the length.

## Set-up

- `count` maps each character to how many times it appears. It is case-sensitive, so `a` and `A` are separate keys.
- `result` is the length built from pairs so far.
- `has_odd` records whether any letter had a leftover single. It is a flag, not a counter, because only one centre exists.

```text
s = "abccccdd"

count   a:1   b:1   c:4   d:2
```

## Step by step

For each count `c`, add `c // 2 * 2` (the letters that form pairs) and check whether `c` is odd.

```text
letter  c   pairs used    result   leftover?
  a     1       0           0        yes  -> has_odd = True
  b     1       0           0        yes
  c     4       4           4        no
  d     2       2           6        no

end:  result = 6, has_odd = True  ->  return 6 + 1 = 7
```

One palindrome of length 7 is `dccaccd`. The single `a` sits in the middle, and `b` is left out.

## Why it works

Each side of a palindrome mirrors the other, so every letter except possibly the centre is used an even number of times. Using `c // 2 * 2` letters takes the largest even number available from each count. Only one letter can sit in the centre, so at most one leftover can be added. Any odd count gives such a leftover, and which one does not matter.

## Where it goes wrong

- Adding 1 for every odd count. With `aaabbbccc` each letter gives a pair (6 total), and there are three odd counts, but the answer is 7, not 9.
- Returning `len(s)` when every letter pairs up is fine, but adding a centre there would be wrong. The flag only turns on for a real leftover, so `aabbcc` gives 6, not 7.
- Ignoring case. `Aa` has two different letters, so the answer is 1.

## Cost

Time O(n) to count, then one pass over the distinct letters. Space O(1): at most 52 distinct letters.

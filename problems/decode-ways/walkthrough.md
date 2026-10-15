## The idea

Each letter is a code from 1 to 26, and a string of digits can often be cut into codes in several ways. The count of ways to decode a prefix depends only on the ways to decode two shorter prefixes: the last character can stand alone as a letter, or the last two characters can form a letter together.

Brute-force recursion recomputes the same prefixes over and over. Counting ways prefix by prefix, shortest first, does each one once, and only the last two counts are ever needed.

## Set-up

- `prev1` is the number of ways to decode the prefix of length `i - 1`. It starts at 1, the empty prefix, which has exactly one (empty) decoding.
- `prev2` is the number of ways for length `i - 2`. It starts at 0 because no such prefix exists yet.
- `cur` is the count for the prefix of length `i`, built from the other two.

Invariant: at the top of round `i`, `prev1` and `prev2` are the correct counts for the two shorter prefixes.

```text
s = "226"
         prev2   prev1
           0       1        (length -1 is impossible, length 0 has 1 way)
```

## Step by step

Two questions each round: is the last digit usable alone (`s[i-1] != "0"`)? Do the last two digits form 10 to 26? Each yes adds a term.

```text
i=1  prefix "2"
     one digit "2" is fine           + prev1 (1)
     two digits: i < 2, skipped
     cur = 1          prev2=1  prev1=1

i=2  prefix "22"
     one digit "2" is fine           + prev1 (1)
     two digits "22" in 10..26       + prev2 (1)
     cur = 2          prev2=1  prev1=2      ("2|2", "22")

i=3  prefix "226"
     one digit "6" is fine           + prev1 (2)
     two digits "26" in 10..26       + prev2 (1)
     cur = 3          prev2=2  prev1=3      ("2|2|6", "22|6", "2|26")
```

The answer is `prev1`, which is 3.

## Why it works

Every decoding of a prefix ends in either a one-digit letter or a two-digit letter. Those two groups do not overlap, and removing that last letter leaves a decoding of a shorter prefix. So the total is the sum of the two shorter counts, each included only when that final piece is a legal letter.

The `0` rules fall out of the conditions. A lone `0` is not a letter, so the one-digit term is skipped. `0` can only help as part of `10` or `20`, which the range check allows.

## Where it goes wrong

Zeros. On `"10"` the one-digit term is skipped at `i=2` (the digit is `0`) but the two-digit term `10` adds `prev2`, giving 1. On `"100"` at `i=3` the one-digit term is skipped and `"00"` is not in 10..26, so `cur` is 0 and the answer is 0.

```text
"100"   i=1: 1   i=2: 1 (via "10")   i=3: 0
```

Using `s[i-2:i] <= 26` without the lower bound would accept `"06"` as 6.

## Cost

Time O(n): one pass. Space O(1): two counters, instead of a full table.

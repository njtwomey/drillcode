## The idea

Can `s` be cut into dictionary words? The first instinct is to try every split, but the number of ways to cut a string grows exponentially. The useful observation is that the question has a shape that repeats: `s` is breakable if its last word is `s[j:i]` and the part before it, `s[:j]`, is itself breakable. So you only ever need to answer the question for prefixes, and each prefix is answered once.

That turns an exponential search into a table with one entry per prefix length.

## Set-up

- `words` is the dictionary as a set, so checking "is this slice a word" is a quick lookup instead of a list scan.
- `longest` is the length of the longest dictionary word. No slice longer than that can match, so the inner loop never needs to look further back than that.
- `dp` has `len(s) + 1` entries. `dp[i]` is True when the prefix `s[:i]` can be split into words.
- `dp[0] = True`: the empty prefix is trivially breakable. This seeds every later entry, because a word that starts at index 0 needs `dp[0]` to be True.

```text
s = "cars"      words = {car, ca, rs}      longest = 3

 index:   0    1    2    3    4
 prefix:  ""   c    ca   car  cars
 dp:      T    F    F    F    F      <- only dp[0] is set
```

## Step by step

For each end position `i`, try each start `j` in `[i - longest, i)`. If `dp[j]` is True and `s[j:i]` is a word, set `dp[i]` and stop.

```text
i=1  j=0: dp[0]=T, "c"    not a word
     dp = [T, F, F, F, F]

i=2  j=0: dp[0]=T, "ca"   is a word  -> dp[2]=T, break
     dp = [T, F, T, F, F]

i=3  j=0: dp[0]=T, "car"  is a word  -> dp[3]=T, break
     dp = [T, F, T, T, F]

i=4  j=1: dp[1]=F, skip
     j=2: dp[2]=T, "rs"   is a word  -> dp[4]=T, break
     dp = [T, F, T, T, T]
```

The answer is `dp[4]`, which is True: `"ca" + "rs"`. Note that `"car"` is a word and `dp[3]` is True, but `"s"` is not a word, so that route dead-ends. The DP did not need to choose in advance. It kept both options alive.

## Why it works

`dp[i]` is True exactly when some split point `j` has `s[:j]` breakable and `s[j:i]` a word. That is the definition of a valid break whose last word ends at `i`. Because `j < i`, every `dp[j]` has already been computed when it is needed.

## Where it goes wrong

- Greedy matching. Always taking the longest or the first matching word can strand the rest of the string, as `"car"` does above.
- Forgetting `dp[0] = True`. Nothing would ever become True.
- Off-by-one on the table size. `dp` needs `len(s) + 1` entries, since there is a prefix for every length from 0 to `len(s)`.
- A string shorter than every word, like `"a"` with `["ab", "abc"]`: the loop finds nothing and `dp[1]` stays False.

## Cost

Time O(n · L), where L is the longest word: n end positions, at most L start positions each, plus a slice and hash of up to L characters (so treat it as O(n · L²) if slicing counts). Space O(n) for `dp`, plus the dictionary set.

## The idea

Any common prefix of all strings is also a prefix of the first one. So the answer is at most the first string, and the only question is where it must be cut short.

Scan column by column. At column `i`, check that every string has a character there and that it matches the first string's. The first column where that fails marks the end of the prefix. This is called a vertical scan.

## Set-up

- `first` is `strs[0]`, the candidate. The answer is some leading slice of it.
- `i` is the current column, and `c` is `first[i]`.
- Nothing else is stored. Invariant: columns before `i` matched in every string.

```text
strs = ["flower", "flow", "flight"]

col    0  1  2  3  4  5
flower f  l  o  w  e  r
flow   f  l  o  w
flight f  l  i  g  h  t
```

## Step by step

```text
i = 0   c = 'f'   flower ok   flow ok   flight ok     keep going
i = 1   c = 'l'   flower ok   flow ok   flight ok     keep going
i = 2   c = 'o'   flower ok   flow ok   flight 'i' != 'o'
        mismatch -> return first[:2] = "fl"
```

A second case where a string is too short, `["abc", "ab"]`:

```text
i = 0   'a'   ok for both
i = 1   'b'   ok for both
i = 2   'c'   "abc" ok, "ab" has len 2 == i  -> too short
        return first[:2] = "ab"
```

If the loop finishes with no mismatch, `first` itself is a prefix of every string, so it is returned whole.

## Why it works

If column `i` fails for some string, no prefix of length `i + 1` or more can be common, and columns before it all matched, so `first[:i]` is the longest common prefix. Checking `i == len(s)` before reading `s[i]` stops the scan safely when a string is shorter, so no index error occurs. An empty string fails at column 0 and returns `""`.

## Where it goes wrong

- Reading `s[i]` before checking the length. A short string would raise an index error.
- Comparing only neighbouring strings with each other and not with `first`. Comparing with `first` is enough and simpler.
- Assuming the loop always returns inside. With a single string or identical strings it finishes, so the final `return first` is needed.

## Cost

Time O(S), where S is the total number of characters, since each character is looked at at most once. Space O(1): only the slice returned.

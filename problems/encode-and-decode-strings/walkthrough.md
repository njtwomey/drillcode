## The idea

We must squash a list of strings into one string and recover the list later. The obvious plan is to join with a separator, but any separator character can appear inside a string, and then the decoder splits in the wrong place. Escaping fixes that but gets messy.

The clean way is to write down how long each string is before the string itself. The decoder then never has to look at the content to find where it ends: it reads a length, skips exactly that many characters, and repeats.

## Set-up

Encoding writes `len(s)`, then `#`, then `s` itself, for each string, all joined together. The `#` only marks the end of the number.

Decoding keeps one variable, `i`, which always sits at the start of a length prefix.

```text
strs    = ["ab", "", "c#d"]
encoded = "2#ab" + "0#" + "3#c#d"
        = "2#ab0#3#c#d"
```

## Step by step

Decode `"2#ab0#3#c#d"`. Indices are shown under the string.

```text
 2 # a b 0 # 3 # c # d
 0 1 2 3 4 5 6 7 8 9 10

Round 1  i=0   first '#' at j=1    length = int("2") = 2
         take s[2:4] = "ab"        i = 1 + 1 + 2 = 4

Round 2  i=4   first '#' at j=5    length = 0
         take s[6:6] = ""          i = 5 + 1 + 0 = 6

Round 3  i=6   first '#' at j=7    length = 3
         take s[8:11] = "c#d"      i = 7 + 1 + 3 = 11

i = 11 = len(s), loop ends.   result = ["ab", "", "c#d"]
```

Round 3 is the interesting one: the payload contains a `#`, but the decoder jumps over it by length and never scans it.

## Why it works

At the start of each round `i` points at a length prefix, because the previous round jumped exactly past the previous payload. A length prefix contains only digits, so the first `#` after `i` is always its terminator, whatever the payloads hold. The slice is then exactly the original string. By induction, every round lands on the next prefix.

An empty string encodes as `0#`, and the slice of length 0 returns `""`. An empty list encodes as `""`, so the loop never runs and the result is `[]`.

## Where it goes wrong

Searching for `#` from the wrong place. If the decoder used `s.split("#")`, the payload `c#d` would be cut in two. The search must start at `i`, and it must be the first `#`, not the last.

Also remember the jump is `j + 1 + length`: past the number, past the `#`, then past the payload.

## Cost

Time O(n) where n is the total characters: each character is written once and read once. Space O(n) for the output.

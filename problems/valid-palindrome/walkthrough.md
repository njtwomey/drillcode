## The idea

A palindrome reads the same from both ends, so compare the first character with the last, the second with the second-to-last, and so on, walking inward. Two pointers do exactly this.

The twist is that spaces, punctuation and letter case are ignored. One way is to build a cleaned copy of the string first. This solution instead skips the junk as it goes, so it needs no extra memory.

## Set-up

- `left` starts at index 0 and `right` at the last index.
- Invariant: every character outside the window `[left, right]` has already been checked (or skipped as junk), so only the window is left to decide.
- The loop runs while `left < right`. When the pointers meet or cross, nothing remains to compare. A single middle character is always equal to itself.

```text
s = "a,b:A"

 index:   0   1   2   3   4
 char:    a   ,   b   :   A
          ^                ^
        left             right
```

## Step by step

Each round does exactly one of three things: skip the left character, skip the right character, or compare and move both.

```text
Round 1   'a' and 'A' are both alphanumeric. Lowercased they match.
          move both inward.

 a   ,   b   :   A
     ^       ^
   left    right

Round 2   s[left] = ',' is not alphanumeric, so left moves.

 a   ,   b   :   A
         ^   ^
       left right

Round 3   s[left] = 'b' is fine, s[right] = ':' is junk, so right moves.

 a   ,   b   :   A
         ^
     left=right
```

Now `left < right` is false, the loop ends, and the answer is `True`.

## Why it works

The window only shrinks, and it shrinks only by discarding characters that either matched their mirror partner or are ignored. If a real mismatch ever appears the function returns `False` immediately. If the window empties without a mismatch, every pair was equal.

## Where it goes wrong

Using `elif` and one skip per round, rather than skipping both sides at once, keeps the bounds safe: after each skip the loop condition `left < right` is checked again, so the pointers cannot run past each other on a string like `".,"`.

```text
s = ".,"      left=0, right=1

Round 1   '.' is junk   left -> 1
Round 2   left == right, loop ends   -> True (nothing to compare)
```

An empty string or all punctuation is therefore a palindrome. Forgetting `.lower()` makes `"Aa"` fail.

## Cost

Time O(n): each round moves at least one pointer, and together they cross the string once. Space O(1): just two indices.

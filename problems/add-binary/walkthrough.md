## The idea

Convert the strings to integers? That breaks the spirit of the task and fails on very long inputs in other languages. The reliable way is schoolbook addition: line the numbers up on the right, add column by column from the least significant bit, and carry.

Because bits are produced from the right, the answer comes out backwards. Collect them in a list and reverse it at the end.

## Set-up

- `i` and `j` point at the current bit of `a` and `b`, starting at the last character of each. A pointer below zero means that string has run out.
- `carry` is 0 or 1, passed to the next column.
- `digits` collects result bits, least significant first.
- The loop runs while either string has bits left or a carry remains. That one condition covers unequal lengths and a final carry out of the top.

```text
a = "11"   b = "1"

 a:  1  1          i -> index 1
 b:     1          j -> index 0
carry = 0
```

## Step by step

In each column, `total = carry + bit of a + bit of b`. The bit written is `total % 2` and the new carry is `total // 2`.

```text
column 0   total = 0 + 1 + 1 = 2    write 0, carry 1
           digits: [0]              i=0  j=-1

column 1   total = 1 + 1 = 2        write 0, carry 1
           (b is exhausted, adds nothing)
           digits: [0, 0]           i=-1 j=-1

column 2   both exhausted, carry is 1 so the loop continues
           total = 1                write 1, carry 0
           digits: [0, 0, 1]

reverse    "100"
```

So `11 + 1 = 100`, which is 3 + 1 = 4.

## Why it works

Each column depends only on the two bits there and the carry from the right. The sum of three bits is at most 3, so the carry never exceeds 1. The loop ends only when both strings are done and no carry remains, so nothing is lost.

## Where it goes wrong

- Looping only while `i >= 0 or j >= 0`. The final carry would be dropped, giving `00` for `11 + 1`.
- Forgetting to reverse. The bits are collected from the right.
- Both inputs `"0"`: the first column gives total 0, so it writes a single `"0"`. The `or "0"` guards the case where no digit is produced at all.

## Cost

Time O(max(m, n)), one step per column. Space O(max(m, n)) for the list of bits and the output string.

## The idea

This is column addition on paper. The lists store digits with the least significant first, which is exactly the order you add in: ones, then tens, then hundreds. So walk both lists together, add the two digits plus the carry from the previous column, write down the last digit, and carry the rest.

You do not need to convert to integers. Lists can be longer than any integer type, and the digit-by-digit method works at any length.

## Set-up

- `dummy` is a throwaway node whose `next` will be the answer. `tail` starts there and always points to the last node written. The dummy saves a special case for the first node.
- `carry` is 0 or 1: the leftover from the previous column.
- The loop is `while l1 or l2 or carry`. It continues while either list has digits, or a carry still needs to be written.

```text
l1:  2 ──▶ 4 ──▶ 3        (342)
l2:  5 ──▶ 6 ──▶ 4        (465)

dummy/tail
   │
   ▼
 [0] ──▶ None             carry = 0
```

## Step by step

Each round: `total = carry + l1 digit + l2 digit`, then `carry, digit = divmod(total, 10)`.

```text
Round 1   2 + 5 + 0 = 7      carry 0, digit 7
  dummy ──▶ 7
            tail

Round 2   4 + 6 + 0 = 10     carry 1, digit 0
  dummy ──▶ 7 ──▶ 0
                  tail

Round 3   3 + 4 + 1 = 8      carry 0, digit 8
  dummy ──▶ 7 ──▶ 0 ──▶ 8
                        tail
```

Both lists are now `None` and `carry` is 0, so the loop ends. Return `dummy.next`, the list `7 → 0 → 8`, which is 807 (342 + 465).

## Why it works

Each round handles one column, and `carry` is the only thing that crosses from one column to the next. A missing digit (a shorter list) is treated as 0 by the `if l1` and `if l2` checks. The sum of two digits and a carry is at most 9 + 9 + 1 = 19, so the carry is never more than 1.

## Where it goes wrong

Stopping when both lists run out. With `5` and `5`:

```text
Round 1   5 + 5 = 10   digit 0, carry 1
lists are empty, but carry is 1

loop on lists only:  0            (wrong, answer should be 10)
loop with carry:     0 ──▶ 1      (right)
```

The result for `[9,9,9,9,9,9,9] + [9,9,9,9]` shows the same thing, with a long carry chain ending in an extra final node.

## Cost

Time O(max(m, n)): one step per digit of the longer list, plus at most one for the final carry. Space O(1) beyond the output list itself.

## The idea

Every value appears twice except one. A hash set or a count table finds the odd one out, but costs O(n) memory. XOR solves it with a single integer, because XOR makes equal values destroy each other.

Three facts about XOR carry the whole solution: `x ^ x = 0`, `x ^ 0 = x`, and the order of operations does not matter. So if you XOR the entire array, each pair collapses to 0, no matter where the two copies sit, and the lone value is all that remains.

## Set-up

- `result` starts at 0, the do-nothing value for XOR.
- Each number is folded in with `result ^= num`.

Invariant: `result` is the XOR of everything seen so far, which equals the XOR of just the values that have appeared an odd number of times.

## Step by step

Take `nums = [4, 1, 2, 1, 2]`:

```text
            result before   num     result after
Round 1       000           100     100   (4)
Round 2       100           001     101   (5)
Round 3       101           010     111   (7)
Round 4       111           001     110   (6)   second 1 undoes the first
Round 5       110           010     100   (4)   second 2 undoes the first
```

The answer is `100`, which is 4. The numbers in between look meaningless, but rounds 4 and 5 each undo an earlier round.

Regrouped, the same computation shows why:

```text
4 ^ 1 ^ 2 ^ 1 ^ 2  =  4 ^ (1 ^ 1) ^ (2 ^ 2)  =  4 ^ 0 ^ 0  =  4
```

## Why it works

XOR is both commutative and associative, so the array can be mentally rearranged into pairs next to each other without changing the result. Each pair is `x ^ x = 0`, zeros disappear, and one value is left. It needs the guarantee that every other value appears exactly twice; with three copies, say, they would not cancel.

## Where it goes wrong

Starting `result` at something other than 0. XOR with a nonzero start leaves that start mixed into the answer:

```text
nums = [2, 2, 1], start result = 5:
5 ^ 2 ^ 2 ^ 1 = 5 ^ 1 = 4     wrong (should be 1)
```

Edge cases are fine as they stand: a single element `[7]` gives `0 ^ 7 = 7`, negatives work because Python's XOR handles them consistently, and when the single value is 0 the result just stays 0 at the end.

## Cost

Time O(n), one pass. Space O(1), one integer.

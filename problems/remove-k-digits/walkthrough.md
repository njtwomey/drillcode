## The idea

To make a number as small as possible, the leftmost digits matter most. So whenever a digit is bigger than the one right after it, deleting that bigger digit improves the number: the smaller one slides into its more significant place. We keep doing that, deleting at most `k` digits in total.

A stack makes this a single pass. The stack holds the digits we are keeping so far, and a new digit pops any larger digits on top of it first.

## Set-up

- `stack` is the kept digits so far. Its invariant: it is non-decreasing, except while we are still paying off pops from `k`.
- `k` counts removals still owed. Each pop spends one.

```text
num = "1432219", k = 3
stack = []    k = 3
```

## Step by step

For each digit, `while k and stack and stack[-1] > digit` pop; then push the digit.

```text
digit  action                          stack         k
 1     push                            [1]           3
 4     push                            [1,4]         3
 3     4 > 3: pop 4, push 3            [1,3]         2
 2     3 > 2: pop 3, push 2            [1,2]         1
 2     2 > 2? no, push                 [1,2,2]       1
 1     2 > 1: pop 2, push 1            [1,2,1]       0
 9     k is 0, push                    [1,2,1,9]     0
```

Result `"1219"`. The deleted digits are 4, 3 and one of the 2s: three, as asked.

If the digits are already non-decreasing nothing pops, so `k` is still owed after the loop. Then the biggest digits are at the end, so trim them:

```text
num = "12345", k = 2:  stack [1,2,3,4,5]  ->  stack[:-2] = [1,2,3]
```

## Why it works

At each position, a smaller digit is always better. If the previous kept digit is larger than the incoming one, dropping it gives a smaller number than keeping it, whatever follows. After the loop the stack is non-decreasing, and in a non-decreasing sequence the best deletions are at the tail. The final `lstrip("0") or "0"` handles two things: leading zeros are not part of the value, and an empty result must read as `"0"`.

## Where it goes wrong

- Not trimming leftovers. For `"12345"` the loop never pops, and returning the stack would delete nothing.
- Leading zeros: `"10200"` with `k = 1` pops the 1, giving the stack `0200`.

```text
"10200", k=1:  stack after loop = [0,2,0,0]
               joined "0200"  ->  lstrip("0")  ->  "200"
```

- `k == len(num)`: everything is removed, the string is empty, and `or "0"` supplies the zero.
- Using `stack[-1] >= digit`: popping equal digits wastes removals for no gain.

## Cost

Time O(n): every digit is pushed once and popped at most once. Space O(n) for the stack.

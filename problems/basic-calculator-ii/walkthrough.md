## The idea

Without parentheses, the only precedence rule is that `*` and `/` bind tighter than `+` and `-`. So think of the expression as a sum of terms. In `3+2*2-4/2` the terms are `3`, `2*2`, and `-(4/2)`. Evaluate each term as it is built and add them all at the end.

A stack of terms does that. For `+` and `-`, push the next number with its sign as a fresh term. For `*` and `/`, do not push; combine the number with the term on top, since it belongs to that term.

## Set-up

- `stack` holds the finished (signed) terms so far. The answer is `sum(stack)`.
- `num` is the number being read, built digit by digit (`num * 10 + digit`).
- `op` is the operator that came before `num`. It starts as `"+"`, so the first number is pushed as a positive term.

The `op` is applied only when we reach the next operator, because only then do we know that `num` is complete. To flush the last number, the loop runs over `s + "+"`; the extra `+` acts as a final operator.

```text
s = "3+2*2-4/2"

stack: []     num: 0     op: +
```

## Step by step

Each row is the moment an operator (or the sentinel) is read. We apply the previous `op` to `num`, then store the new operator.

```text
read   num   op applied     stack after
 +     3     +  push 3      [3]
 *     2     +  push 2      [3, 2]
 -     2     *  2 * 2       [3, 4]
 /     4     -  push -4     [3, 4, -4]
 +     2     /  -4 / 2      [3, 4, -2]    (sentinel)

sum([3, 4, -2]) = 5
```

Digits just grow `num` between rows, and spaces are skipped. A two-digit number such as `12` goes `1`, then `1 * 10 + 2 = 12`.

## Why it works

Every `+` or `-` starts a new term, and every `*` or `/` extends the latest term, which is the top of the stack. At the end, each stack entry is a complete term with its sign, so adding them gives the value of the whole expression.

## Where it goes wrong

- Division must truncate toward zero. Python's `//` floors, so `-3 // 2` is `-2`, not `-1`. The code divides the absolute value and reapplies the sign.

```text
top = -3, num = 2
floor:     -3 // 2        = -2     wrong
truncate:  -(abs(-3) // 2) = -1    right
```

- Without the sentinel, the final number is never applied.
- Applying `op` when the number is read, instead of when the next operator arrives, uses the wrong operator.

## Cost

Time O(n): one pass over the characters. Space O(n) for the stack of terms (O(1) is possible by keeping only the last term and a running total).

## The idea

With only `+` and `-` there is no precedence to worry about. The only thing a parenthesis does is apply a sign to everything inside it: `a - (b + c)` is `a - b - c`.

So scan left to right, keep a running total, and remember the sign of the next number. When a `(` opens, park the outer total and the sign in front of the bracket, then start a fresh total inside. When the matching `)` arrives, finish the inner total, multiply it by the parked sign, and add it back to the parked outer total.

## Set-up

- `result` is the total of the current bracket level, not counting the number still being read.
- `sign` is `1` or `-1`, the sign that applies to the number being read.
- `num` accumulates digits, so `10` is read as `1` then `10`.
- `stack` holds pairs pushed as `result` then `sign`, and popped in the reverse order.

```text
s = "1-(2-3)+4"

result 0   sign +1   num 0   stack []
```

## Step by step

The state after each character:

```text
char   result  sign  num   stack
 1       0      +1    1    []         read digit
 -       1      -1    0    []         commit 1, next sign is minus
 (       0      +1    0    [1, -1]    park total 1 and sign -1, start fresh
 2       0      +1    2    [1, -1]
 -       2      -1    0    [1, -1]    commit 2, next sign is minus
 3       2      -1    3    [1, -1]
 )       2      -1    0    []         see below
 +       2      +1    0    []
 4       2      +1    4    []
```

The `)` step: add the pending number, `result = 2 + (-1 * 3) = -1`. Multiply by the parked sign `-1`, giving `1`. Add the parked total `1`, giving `2`. After the loop, `result + sign * num = 2 + 4 = 6`, and indeed `1 - (2 - 3) + 4 = 6`.

## Why it works

Inside a bracket, the code is solving a smaller copy of the same problem with a fresh total. When the bracket closes, that inner value is a single number, and the parked sign says whether it is added or subtracted. Nesting just means the stack gets deeper.

A leading minus needs no special case. At the start of the string, or right after `(`, `num` is `0` when the `-` arrives, so committing it adds nothing, and the sign flips for the number that follows. That makes `-(2+3)` and `1-(-2)` work.

## Where it goes wrong

- Forgetting the final `result + sign * num`. The last number is never followed by an operator, so nothing commits it inside the loop.
- Popping in the wrong order. The sign was pushed last, so it comes off first.
- Not resetting `result` and `sign` after `(`, which leaks the outer total into the bracket.

## Cost

Time O(n), one pass over the string. Space O(n) for the stack when brackets nest deeply.

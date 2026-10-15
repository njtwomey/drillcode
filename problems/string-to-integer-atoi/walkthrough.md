## The idea

Parsing a number from text is easiest as a short pipeline of phases that each consume part of the string and never look back: skip spaces, take an optional sign, read digits, clamp. One index `i` moves left to right through all four. Nothing needs a regex or a second pass.

The rules that make it fiddly (a second sign means "no number", letters after the digits are ignored, huge values clamp) all fall out naturally from the phases if each one only does its own job.

## Set-up

- `i` is the position of the next unread character, and `n` is the length.
- `sign` is `1` unless the sign phase sees `-`.
- `result` is the digits read so far, as a non-negative number.
- `INT_MAX` and `INT_MIN` are the clamp bounds, `2**31 - 1` and `-2**31`.

```text
s = "  -042x"
     0123456
i = 0   sign = 1   result = 0
```

## Step by step

```text
Phase 1  skip spaces        i: 0 -> 1 -> 2        s[2] = '-'
              ^ i

Phase 2  one optional sign  s[2] is '-': sign = -1, i -> 3
                ^ i

Phase 3  read digits        s[3]='0'  result = 0
                            s[4]='4'  result = 4
                            s[5]='2'  result = 42
                            s[6]='x'  not a digit: stop

Phase 4  clamp              sign * result = -42, inside the range
```

Two other inputs show why the phases behave as they do:

```text
"+-12"   phase 2 takes '+', i=1. Phase 3 sees '-', not a digit,
         reads nothing. result = 0.  Answer 0.

"-91283472332"  digits keep building until result passes 2**31:
         9, 91, ..., 912834723, 9128347233 > 2147483648 -> break
         clamp: max(INT_MIN, min(INT_MAX, -9128347233)) = -2147483648
```

## Why it works

Each phase consumes only the characters it owns and leaves `i` at the start of the next phase's input. A second sign lands in phase 3 where it is not a digit, so zero digits are read, and zero is the right answer. Empty, all-space and sign-only strings also read zero digits, so `result` stays 0 without special cases.

The loop stops growing `result` as soon as it exceeds `INT_MAX + 1`. At that point the final clamp will give the same answer whatever the remaining digits are, so there is no need to keep multiplying.

## Where it goes wrong

- Using `str.isdigit()`. It accepts some Unicode characters that `int()` cannot parse, so the code compares against `"0"` and `"9"` instead.
- Clamping the magnitude to `INT_MAX` before applying the sign. A negative number can reach `-2**31`, whose magnitude is one more than `INT_MAX`, so the clamp must come after `sign * result`.

```text
"-2147483648"   result = 2147483648
   clamp result to INT_MAX first: -2147483647  (wrong)
   sign * result, then clamp:     -2147483648  (right)
```

- Skipping tabs or newlines as well as spaces. Only the space character counts here.

## Cost

Time O(n): `i` moves forward once. Space O(1): a handful of integers. Python does not overflow, so the early `break` is about keeping numbers small, not about correctness of the arithmetic.

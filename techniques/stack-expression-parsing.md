---
title: Stack for expressions and nested repeats
area: Stacks
topics: [Stack, String]
problems:
  - evaluate-reverse-polish-notation
  - basic-calculator-ii
  - decode-string
related: [stack-matching, monotonic-stack]
---
## Reach for it when
- The input is a string with numbers, operators and precedence (`*` and `/` before `+` and `-`).
- The input has nested groups that repeat, such as `3[a2[c]]`.
- You must read a multi-digit number one character at a time.
- Something must be remembered while a nested part is processed, then restored.

## Setup
- `stack = []`: the saved partial state. Invariant: the top belongs to the level just outside the one being scanned.
- `num = 0`: the number being read. Each digit does `num = num * 10 + int(ch)`.
- `op = "+"`: the operator seen before `num`. It is applied when the next operator arrives, so the pending operator is always one step behind the scan.
- For nested repeats, `curr = ""` is the text built at the current level, and a frame is the pair `(curr, num)` saved on `[`.
- Append a sentinel (`s + "+"`) so the last number is flushed by the same code as every other.

## Template
```python
def calculate(s):
    stack = []
    num = 0
    op = "+"
    for ch in s + "+":
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch == " ":
            continue
        else:
            if op == "+":
                stack.append(num)
            elif op == "-":
                stack.append(-num)
            elif op == "*":
                stack.append(stack.pop() * num)
            else:
                top = stack.pop()
                quotient = abs(top) // num
                stack.append(quotient if top >= 0 else -quotient)
            op = ch
            num = 0
    return sum(stack)
```

## What it removes
It removes building a parse tree and handling precedence by cases. Terms are signed numbers that are summed at the end, and `*` and `/` fold into the top term at once, so precedence is one branch. For nested repeats it removes recursion: the frame stack stands in for the call stack.

## Pitfalls
- Applying the current character as the operator instead of `op`. The operator that belongs to `num` is the previous one. `"3-2"` gives 5 if you apply `-` to the wrong side.
- No sentinel: the last number is never pushed and `"1+2"` returns 1.
- Not resetting `num = 0` after an operator, so the next number is glued onto the old one.
- Floor division on negatives. Python's `-7 // 2` is -4, but the statement truncates toward zero. `basic-calculator-ii` uses `abs(top) // num` and restores the sign.
- Spaces: skip them with `continue` before the operator branch, or a space triggers an operator step.
- Single-digit parsing: `"12"` read as two numbers. Multi-digit counts like `100[a]` need `num * 10`.
- In `decode-string`, pushing `curr` but not `num`, or not resetting both after `[`. The frame must hold both, and `curr, num = "", 0` starts the inner level clean.
- Reading `stack[0]` of an RPN stack after a bad expression: a valid one leaves exactly one value.

## Variants
- Postfix (`evaluate-reverse-polish-notation`): no precedence and no `op`. Push numbers. On an operator, pop `b` then `a` and push the result, using `int(a / b)` to truncate toward zero. Listed also on `stack-matching`.
- Calculator with precedence (`basic-calculator-ii`): the template. `stack` holds terms. `+` pushes `num`, `-` pushes `-num`, `*` and `/` rewrite the top. The answer is `sum(stack)`. The sentinel `"+"` flushes the last number.
- Nested repeats (`decode-string`): `stack` holds `(curr, num)` frames. On `[`, push `(curr, num)` and reset both. On `]`, `prev, count = stack.pop()` and `curr = prev + curr * count`. Letters extend `curr`. The answer is `curr` after the loop.

## Worked example
Problem: `basic-calculator-ii`

Each term is pushed signed, or merged into the top term when the pending operator binds tighter.

```python
class Solution:
    def calculate(self, s: str) -> int:
        stack = []
        num = 0
        op = "+"
        for ch in s + "+":
            if ch.isdigit():
                num = num * 10 + int(ch)
            elif ch == " ":
                continue
            else:
                if op == "+":
                    stack.append(num)
                elif op == "-":
                    stack.append(-num)
                elif op == "*":
                    stack.append(stack.pop() * num)
                else:
                    top = stack.pop()
                    quotient = abs(top) // num
                    stack.append(quotient if top >= 0 else -quotient)
                op = ch
                num = 0
        return sum(stack)
```

This is the template with a class wrapper. `op` starts as `"+"`, so the first number is pushed as a positive term. After each step `op = ch` stores the operator for the number that follows. The appended `"+"` flushes the final `num`. The `else` branch for `/` truncates toward zero with `abs`.

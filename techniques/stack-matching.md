---
title: Stack for nesting and postfix
area: Stacks
topics: [Stack]
problems:
  - valid-parentheses
  - evaluate-reverse-polish-notation
  - min-stack
  - implement-queue-using-stacks
related: [monotonic-stack, design-structures]
---
## Reach for it when
- The input has brackets or other nesting.
- The wording is "most recent unmatched" or "last in, first out".
- The input is a postfix or prefix expression.
- You need undo, or a queue built from stacks.

## Setup
- `stack = []`: the openers (or operands) still waiting. Invariant: the top is the most recent unmatched item.
- `pairs`, when matching brackets: a dict keyed by closer, `{")": "(", "]": "[", "}": "{"}`, so `ch in pairs` also says whether `ch` is a closer.
- Push openers. On a closer, pop and compare. At the end, the answer needs `not stack`.

## Template
```python
def is_balanced(s):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
        else:
            stack.append(ch)
    return not stack
```

## What it removes
It removes the repeated search for the nearest unmatched opener: LIFO order puts it on top. In postfix evaluation it removes parsing and precedence rules, because the operands an operator needs are the two on top. In `implement-queue-using-stacks`, lazy transfer removes the O(n) cost per pop: each element moves across once, so operations are amortised O(1).

## Pitfalls
- Popping an empty stack on a closer: `")"` raises `IndexError`. Test `not stack` first, as in the template.
- Returning `True` without the final `not stack`: `"(("` passes.
- In RPN, swapping operand order: `b = stack.pop()` comes first (the right operand), then `a`. Reversed, `"3 4 -"` gives 1 instead of -1.
- In RPN, using `a // b` for division: it floors, so `-7 / 2` gives -4 instead of -3. Use `int(a / b)`.
- In `implement-queue-using-stacks`, refilling `out_stack` while it is not empty: newer items end up under older ones and FIFO order breaks.
- In the same problem, `empty` checking only one stack.

## Variants
- Bracket matching (`valid-parentheses`): the template.
- Postfix evaluation (`evaluate-reverse-polish-notation`): push numbers, and on an operator pop two and push the result. A valid expression leaves one value.
- Stack with a running minimum (`min-stack`): the solution stores `(val, current_min)` tuples on one stack, so the minimum is restored on `pop` with no search. A parallel stack that gets a push only when the value is `<=` the current minimum also works, but the solution does not use it.
- Two-stack queue (`implement-queue-using-stacks`): push to `in_stack`, pop from `out_stack`, and refill `out_stack` from `in_stack` only when it is empty.

## Worked example
Problem: `evaluate-reverse-polish-notation`

Operands wait on the stack until an operator takes the two most recent ones.

```python
class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        stack = []
        for token in tokens:
            if token in ("+", "-", "*", "/"):
                b = stack.pop()
                a = stack.pop()
                if token == "+":
                    stack.append(a + b)
                elif token == "-":
                    stack.append(a - b)
                elif token == "*":
                    stack.append(a * b)
                else:
                    stack.append(int(a / b))
            else:
                stack.append(int(token))
        return stack[0]
```

`stack` is the template's, holding operands instead of openers. The operator branch is the "closer" case: it pops, here two items, and pushes the result back. The last line plays the part of the final emptiness check. A valid expression leaves exactly one value, the answer.

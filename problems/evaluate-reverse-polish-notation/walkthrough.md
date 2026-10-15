## The idea

In reverse Polish notation an operator comes after its two operands: `2 1 +` means `2 + 1`. There are no brackets and no precedence rules, because the order of the tokens already says what to do.

That makes a stack the natural tool. Reading left to right, push every number. When an operator arrives, the two most recent numbers are its operands: pop them, combine them, push the result back. The result may itself be an operand for a later operator.

## Set-up

- `stack` holds values that are waiting for an operator.

Invariant: after each token, `stack` holds the values of all complete sub-expressions read so far that have not yet been consumed. For a valid expression, one value is left at the end.

```text
tokens = ["2", "1", "+", "3", "*"]        (this means (2 + 1) * 3)

stack = []
```

## Step by step

```text
token "2"   number: push 2                stack = [2]
token "1"   number: push 1                stack = [2, 1]
token "+"   operator: b = pop() = 1
                      a = pop() = 2
                      push a + b = 3      stack = [3]
token "3"   number: push 3                stack = [3, 3]
token "*"   operator: b = pop() = 3
                      a = pop() = 3
                      push a * b = 9      stack = [9]
```

The answer is `stack[0]`, which is 9.

## Why it works

Every operator needs exactly two operands, and in postfix form those are the two most recently produced values: the top two entries. Popping them in order and pushing the result replaces a whole sub-expression with its value, which is what the next operator will see. Nesting needs no extra work, because inner expressions finish first.

## Where it goes wrong

The order of the pops. The first pop is the right operand `b`, the second is the left operand `a`. For `+` and `*` it does not matter, but for `-` and `/` it does:

```text
tokens ["5", "2", "-"]     stack [5, 2]
  b = 2, a = 5             a - b = 3     correct
  swapped: 2 - 5 = -3                    wrong
```

Division must truncate toward zero. Python's `//` floors, so `-7 // 2` gives `-4`, but the required answer is `-3`.

```text
tokens ["-7", "2", "/"]
  int(-7 / 2) = int(-3.5) = -3     correct
  -7 // 2                 = -4     wrong
```

Negative numbers like `"-11"` are tokens, not operators, which is why the check is for the exact strings `+ - * /` and everything else goes through `int(token)`.

## Cost

Time O(n): each token is handled once with constant work. Space O(n) for the stack in the worst case, such as many numbers followed by many operators.

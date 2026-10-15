Evaluate the arithmetic expression string `s` and return its integer value. The expression contains non-negative integers, the binary operators `+`, `-`, `*`, `/`, and arbitrary spaces. Operator precedence applies (`*` and `/` before `+` and `-`, left to right among equals), and integer division truncates toward zero. There are no parentheses and no unary minus.

`s` is always a valid expression, and every intermediate value fits in a 32-bit signed integer. You may not use `eval` or similar built-ins.

Constraints:
- `1 <= len(s) <= 3 * 10^5`
- Numbers can have many digits, and `s` may start or end with spaces
- Division by zero does not occur

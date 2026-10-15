Evaluate the arithmetic expression string `s` and return its integer value. The expression contains non-negative integers, the operators `+` and `-`, parentheses, and spaces, and you may not use `eval` or any built-in expression evaluator.

A `-` can also act as a unary minus, for example at the start of the expression or directly after an opening parenthesis (`-(2+3)` or `1-(-2)`). Every expression is valid, and intermediate and final values fit in a signed 32-bit integer.

Constraints:
- `1 <= len(s) <= 3 * 10^5`
- Parentheses may be nested deeply
- No `*` or `/` operators

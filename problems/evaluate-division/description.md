Each pair `equations[i] = [a, b]` with `values[i]` states that `a / b = values[i]`, where the variables are strings and the equations are mutually consistent.

For each pair `[c, d]` in `queries`, return the value of `c / d`, or `-1.0` if it cannot be determined from the equations. A variable that does not appear in any equation is unknown, even when asked for itself. Return the answers as a list of floats.

Constraints:
- `1 <= len(equations), len(queries) <= 20`
- `0.0 < values[i] <= 20.0`
- Variable names have at most 5 characters; there is no division by zero.

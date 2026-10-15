A lock has four circular wheels, each showing a digit `0`-`9`. Turning a wheel one step moves its digit up or down by one, wrapping from `9` to `0` and from `0` to `9`. The lock starts at `"0000"`.

`deadends` lists states that jam the lock: reaching one stops all further turning. Return the minimum number of turns needed to reach the string `target`, or `-1` if it is impossible.

Constraints:
- `1 <= len(deadends) <= 500`
- All strings have length 4 and consist of digits.
- `target` is not in `deadends`.

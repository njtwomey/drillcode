Given a string `s` made only of `'('`, `')'` and `'*'`, decide whether it can be read as a valid parenthesis sequence. Each `'*'` may independently stand for `'('`, `')'` or the empty string. A sequence is valid when every `'('` is closed by a later `')'`, every `')'` closes an earlier `'('`, and the string may be empty. Return `True` if some assignment of the stars makes `s` valid, otherwise `False`.

Constraints:
- `1 <= len(s) <= 100`
- Aim for a single pass with O(1) extra space

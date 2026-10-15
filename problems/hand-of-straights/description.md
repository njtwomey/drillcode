Alice holds cards whose values are listed in `hand`. She wants to split all of them into groups of exactly `groupSize` cards, where the values in each group are consecutive integers (for example 4, 5, 6). Every card must be used once. Return `True` if such a split exists, otherwise `False`.

Constraints:
- `1 <= len(hand) <= 10^4`
- `0 <= hand[i] <= 10^9`
- `1 <= groupSize <= len(hand)`
- Values may repeat

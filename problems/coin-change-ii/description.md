Given a target `amount` and a list of distinct coin denominations `coins`, return the number of different combinations of coins that sum exactly to `amount`. Each denomination can be used any number of times, and combinations that differ only in order count as the same one. If no combination works, return 0. Making amount 0 counts as one combination. The answer fits in a signed 32-bit integer.

Constraints:
- `1 <= len(coins) <= 300`
- `1 <= coins[i] <= 5000`, all distinct
- `0 <= amount <= 5000`

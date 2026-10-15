There are `n` stations on a circular route. Station `i` gives you `gas[i]` units of fuel, and driving from station `i` to station `i + 1` (wrapping around) costs `cost[i]`. Your tank is unlimited but starts empty.

Return the index of the station from which you can complete one full lap clockwise, or `-1` if no starting station works. If a solution exists it is guaranteed to be unique.

Constraints:
- `n == len(gas) == len(cost)`
- `1 <= n <= 10^5`
- `0 <= gas[i], cost[i] <= 10^4`

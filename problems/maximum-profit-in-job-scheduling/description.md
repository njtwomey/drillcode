There are `n` jobs, where job `i` runs from `startTime[i]` to `endTime[i]` and pays `profit[i]`. Choose a subset of jobs such that no two chosen jobs overlap in time, and return the maximum total profit. A job that starts at the exact moment another one ends does not overlap with it.

Constraints:
- `1 <= n <= 5 * 10^4`
- `1 <= startTime[i] < endTime[i] <= 10^9`
- `1 <= profit[i] <= 10^4`
- The three arrays have the same length and are in no particular order

You are given an array `tasks` of single uppercase letters, where each letter is a task type, and a cooldown `n`. The CPU runs one task or sits idle in each time unit. Tasks may be run in any order, but two runs of the same type must have at least `n` time units between them.

Return the minimum number of time units needed to finish every task, counting idle units.

Constraints:
- `1 <= len(tasks) <= 10^4`
- Each task is an uppercase letter `A` to `Z`
- `0 <= n <= 100`

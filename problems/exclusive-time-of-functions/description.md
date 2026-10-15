A single-threaded CPU runs `n` functions with ids `0..n-1`. You are given `logs`, a chronological list of strings of the form `"id:start:timestamp"` or `"id:end:timestamp"`, recording when a call begins and when it ends. A function may call others, including itself, and starting a call pauses the caller until the callee ends.

A call that starts at time `s` and ends at time `e` occupies the CPU for the whole of both time units. Return an array where entry `i` is the total time function `i` spent actively running, excluding time its callees ran.

Constraints:
- `1 <= n <= 100`
- `1 <= len(logs) <= 500`
- Logs are valid and well nested; timestamps are non-decreasing

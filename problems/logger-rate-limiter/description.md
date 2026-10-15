Design a `Logger` that decides whether each incoming message may be printed. A given message may be printed at most once every 10 seconds.

`shouldPrintMessage(timestamp, message)` returns `true` if `message` should be printed at `timestamp`, and `false` if the same message was printed less than 10 seconds earlier. A message printed at time `t` can be printed again from time `t + 10`. Messages that are not printed do not count as printed.

Calls arrive in non-decreasing order of `timestamp`, and several calls may share a timestamp.

Constraints:
- `0 <= timestamp <= 10^9`
- Messages are short lowercase strings
- At most `10^4` calls

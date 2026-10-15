Design a `HitCounter` that counts hits on a web page during the most recent 5 minutes.

`hit(timestamp)` records one hit at `timestamp`, given in seconds. `getHits(timestamp)` returns the number of hits in the past 300 seconds, that is, those with a time in `[timestamp - 299, timestamp]`.

Calls come in chronological order, so `timestamp` never decreases between calls. Several hits can share the same timestamp, and each counts separately.

Constraints:
- `1 <= timestamp <= 2 * 10^9`
- At most `300` calls in total
- Think about how the structure would behave if hits arrived in the millions

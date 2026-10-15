A network has `n` nodes labelled `1..n`. `times` lists directed edges `[u, v, w]`: a signal sent from `u` reaches `v` after `w` time units. A signal is sent from node `k` at time 0.

Return the minimum time until every node has received it, or `-1` if some node can never receive it.

Constraints:
- `1 <= k <= n <= 100`
- `1 <= len(times) <= 6000`
- `0 <= w <= 100`
- Each pair `(u, v)` appears at most once.

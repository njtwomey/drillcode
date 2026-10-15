You are given an array `w` of positive integers, where `w[i]` is the weight of index `i`.

Implement a class `Solution` whose constructor `Solution(w)` receives the weights, and whose method `pickIndex()` returns a random index in the range `[0, w.length - 1]`. Index `i` must be returned with probability `w[i] / sum(w)`, and each call is independent of the others.

For example, with weights `[1, 3]` index `0` is chosen about 25% of the time and index `1` about 75% of the time.

Constraints:
- `1 <= w.length <= 10^4`
- `1 <= w[i] <= 10^5`
- At most `10^4` calls to `pickIndex`

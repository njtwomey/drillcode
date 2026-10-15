Given the `root` of a binary tree and an integer `targetSum`, return how many paths have node values summing to `targetSum`. A path must go downward, from a node to one of its descendants (parent to child only), but it may start and end at any node, not just the root and a leaf. A single node counts as a path of length one.

Constraints:

- Up to 1000 nodes
- Node values lie in [-10^9, 10^9] and can be negative, so a running sum is not monotonic
- `targetSum` lies in [-1000, 1000]

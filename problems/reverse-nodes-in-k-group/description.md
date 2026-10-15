Given the `head` of a singly linked list and an integer `k`, reverse the nodes in consecutive blocks of `k` and return the new head. Blocks are taken from the front; if fewer than `k` nodes remain at the end, those nodes keep their original order.

Reverse by relinking nodes; do not change their values. The list is non-empty and `k` does not exceed its length.

Constraints:

- List length `n` is at most 5000
- `1 <= k <= n`
- Aim for O(1) extra memory

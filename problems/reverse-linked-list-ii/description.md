Given the `head` of a singly linked list and two 1-indexed positions `left <= right`, reverse the nodes from position `left` through position `right` inclusive, leave the rest of the list as it is, and return the head of the result.

Both positions are valid for the list. When `left == right` nothing changes. The head itself may be part of the reversed segment.

Constraints:

- List length `n` is between 1 and 500
- `1 <= left <= right <= n`
- A single pass over the list is expected

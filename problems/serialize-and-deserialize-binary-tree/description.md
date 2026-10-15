Implement a `Codec` with two methods:

- `serialize(root)` converts a binary tree into a string.
- `deserialize(data)` converts a string produced by `serialize` back into a tree structurally identical to the original, with the same values; return its root (`None` for an empty tree).

The string format is up to you, but `deserialize` must work from the string alone, with no state kept in the `Codec` instance.

Constraints:
- Between 0 and `10^4` nodes
- Node values lie in [-1000, 1000]

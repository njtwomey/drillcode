Implement `LRUCache`, a fixed-capacity cache that evicts the least recently used entry.

- `LRUCache(capacity)`: create an empty cache holding at most `capacity` entries.
- `get(key)`: return the value stored for `key`, or `-1` if absent. A hit makes `key` the most recently used.
- `put(key, value)`: insert or overwrite `key`, making it the most recently used. If the insert pushes the size past `capacity`, evict the least recently used key. Returns nothing.

Constraints:
- `1 <= capacity <= 3000`
- Up to `2 * 10^5` calls
- `get` and `put` must each run in O(1) average time

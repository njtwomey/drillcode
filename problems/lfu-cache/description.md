Implement `LFUCache`, a fixed-capacity cache that evicts the least frequently used key.

- `LFUCache(capacity)`: create an empty cache. A capacity of 0 stores nothing.
- `get(key)`: return the value for `key`, or `-1` if absent. A hit counts as one use.
- `put(key, value)`: insert or overwrite `key`; this counts as one use. If inserting a new key exceeds `capacity`, first evict the key with the fewest uses; among ties evict the least recently used one. A newly inserted key starts with a single use. Returns nothing.

Constraints:
- `0 <= capacity <= 10^4`
- Up to `2 * 10^5` calls
- Each of `get` and `put` must run in O(1) average time

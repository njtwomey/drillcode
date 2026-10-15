Implement `TimeMap`, a key-value store that keeps every historical value of a key along with the time it was written.

- `TimeMap()`: create an empty store.
- `set(key, value, timestamp)`: record that `key` held `value` from `timestamp` onward. Returns nothing.
- `get(key, timestamp)`: return the value from the `set` call with the largest stored timestamp that is `<= timestamp`. If `key` is unknown or all its timestamps are later, return `""`.

Constraints:
- `set` timestamps for a given key are strictly increasing across calls
- `1 <= timestamp <= 10^7`
- Up to `2 * 10^5` calls in total, so `get` should be better than a linear scan

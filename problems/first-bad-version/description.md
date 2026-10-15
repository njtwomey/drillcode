Versions `1` through `n` were released in order. From some version onward every version is bad. You can query a predefined `isBadVersion(version)` that returns whether a version is bad. Return the number of the first bad version, as a 1-based version number. At least one bad version exists.

Constraints:

- `1 <= n <= 2^31 - 1`
- Minimize the number of `isBadVersion` calls
- Beware of integer overflow in other languages

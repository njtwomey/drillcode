Implement a `Codec` class with two methods:

- `encode(strs)` takes a list of strings and returns a single string.
- `decode(s)` takes the output of `encode` and returns the original list of strings, in the same order, including empty strings and the empty list.

The codec must be stateless: `decode` may rely only on the string it is given, and no instance state or global state may carry data between the two calls.

Constraints:
- `0 <= len(strs) <= 200`
- `0 <= len(strs[i]) <= 200`
- Strings may contain any of the 256 ASCII characters, so no character can be assumed absent.

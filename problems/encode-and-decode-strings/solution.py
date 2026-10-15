"""Encode and Decode Strings (#271, medium)

Approach: Prefix each string with its length and a delimiter, e.g. "4#word".
Tricks: Length-prefixing copes with any character, including the delimiter.
Edge cases:
  - Empty strings in the list
  - Empty list
  - Strings containing '#'

Time O(n), space O(n).
"""


class Codec:
    def encode(self, strs: List[str]) -> str:
        """Encodes a list of strings to a single string."""
        # Length first, then the text. The decoder never inspects the text itself, so any
        # characters (including '#' or digits) are safe.
        return "".join(f"{len(s)}#{s}" for s in strs)

    def decode(self, s: str) -> List[str]:
        """Decodes a single string to a list of strings."""
        result = []
        # i always sits at the start of a length prefix.
        i = 0
        while i < len(s):
            # First '#' after i ends the length. The payload can't confuse this, because we
            # skip over it by length rather than scanning it.
            j = s.index("#", i)
            length = int(s[i:j])
            # Slice exactly `length` chars; works for empty strings (length 0) too.
            result.append(s[j + 1:j + 1 + length])
            i = j + 1 + length
        return result

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
        return "".join(f"{len(s)}#{s}" for s in strs)

    def decode(self, s: str) -> List[str]:
        """Decodes a single string to a list of strings."""
        result = []
        i = 0
        while i < len(s):
            j = s.index("#", i)
            length = int(s[i:j])
            result.append(s[j + 1:j + 1 + length])
            i = j + 1 + length
        return result

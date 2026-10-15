"""Maximum XOR of Two Numbers in an Array (#421, medium)

Approach: Binary trie of the bits, most significant first; for each number walk the
    opposite bit whenever it exists.
Tricks: A higher bit outweighs all lower ones, so greedily preferring the opposite bit
    is optimal; limit depth to the max's bit length.
Edge cases:
  - Single element gives 0
  - All duplicates
  - Values at 2^31 - 1 and 0

Time O(n * B), space O(n * B).
"""

class Solution:
    def findMaximumXOR(self, nums: List[int]) -> int:
        # Binary trie of the numbers, most significant bit first. Each node is a dict
        # {bit: child}. To maximise x ^ y, walk down choosing at every level the child
        # whose bit is the opposite of x's bit when it exists: a 1 in a higher position
        # outweighs everything below it, so taking it greedily is optimal.
        bits = max(nums).bit_length()  # higher bits are zero for every number
        root = {}
        for num in nums:
            node = root
            for shift in range(bits - 1, -1, -1):
                node = node.setdefault((num >> shift) & 1, {})
        best = 0
        for num in nums:
            node = root
            current = 0
            for shift in range(bits - 1, -1, -1):
                bit = (num >> shift) & 1
                # Prefer the opposite bit: it makes this bit of the XOR a 1.
                if 1 - bit in node:
                    current |= 1 << shift
                    node = node[1 - bit]
                else:
                    node = node[bit]
            best = max(best, current)
        return best

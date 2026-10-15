"""Palindrome Linked List (#234, easy)

Approach: Find the middle with slow and fast pointers, reverse the second half in place,
    then compare both halves.
Tricks: Only the reversed half needs to be walked; for odd lengths the middle node
    compares equal to itself so no special case is needed.
Edge cases:
  - Single node
  - Odd and even lengths
  - Ends match but the centre differs

Time O(n), space O(1).
"""

class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        # Phase 1: find the middle. When fast runs off the end, slow is at the start
        # of the second half (for an odd length, at the middle node itself).
        slow, fast = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        # Phase 2: reverse from slow onward so the second half can be read from the
        # tail backwards without extra memory. prev ends as the reversed head.
        prev = None
        while slow:
            nxt = slow.next  # save before overwriting the link
            slow.next = prev
            prev = slow
            slow = nxt
        # Phase 3: compare the first half with the reversed second half. The reversed
        # half is never longer than the first, so looping on it is enough; for an odd
        # length the shared middle node just compares equal to itself.
        left, right = head, prev
        while right:
            if left.val != right.val:
                return False
            left = left.next
            right = right.next
        return True

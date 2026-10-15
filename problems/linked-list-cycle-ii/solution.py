"""Linked List Cycle II (#142, medium)

Approach: Floyd's cycle detection, then restart one pointer at the head and advance both
    one step at a time until they meet at the entry.
Tricks: The distance from head to the entry equals the distance from the meeting point
    to the entry (mod the cycle length), so the second phase walks both pointers at the
    same speed.
Edge cases:
  - Empty list or single node without a cycle
  - Tail points to itself
  - Cycle starts at the head

Time O(n), space O(1).
"""

class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # Phase 1: Floyd's tortoise and hare. If there is a cycle the fast pointer
        # laps the slow one inside it, so they must meet; if not, fast reaches null.
        slow, fast = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                # Phase 2: let a = distance from head to the cycle entry and c = the
                # cycle length. At the meeting point slow has walked a + k and fast
                # 2(a + k), so a + k is a multiple of c. Walking a more steps from the
                # meeting point therefore lands exactly on the entry, and a pointer
                # from the head reaches it after the same a steps.
                slow = head
                while slow is not fast:
                    slow = slow.next
                    fast = fast.next
                return slow
        return None

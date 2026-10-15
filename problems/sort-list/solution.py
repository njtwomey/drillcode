"""Sort List (#148, medium)

Approach: Top-down merge sort, splitting at the middle found with slow and fast pointers
    and merging the sorted halves with a dummy head.
Tricks: Cut the list at the end of the first half before recursing; starting fast one
    node ahead makes two-node lists split 1 and 1 so recursion always shrinks.
Edge cases:
  - Empty list and single node
  - Already sorted and reverse sorted
  - Duplicates and negatives
  - Two and three nodes

Time O(n log n), space O(log n).
"""

class Solution:
    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # Merge sort suits linked lists: splitting needs no random access and merging
        # relinks nodes without extra storage. A list of 0 or 1 nodes is sorted.
        if head is None or head.next is None:
            return head
        # Split in the middle. Starting fast one step ahead makes slow stop at the
        # END of the first half; with two nodes that gives halves of 1 and 1, which
        # guarantees both halves are strictly smaller and the recursion terminates.
        slow, fast = head, head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        second = slow.next
        slow.next = None  # cut the list so the first half really ends here
        return self.merge(self.sortList(head), self.sortList(second))

    def merge(self, a: Optional[ListNode], b: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0)
        tail = dummy
        while a and b:
            # Taking from a on ties keeps the sort stable.
            if a.val <= b.val:
                tail.next, a = a, a.next
            else:
                tail.next, b = b, b.next
            tail = tail.next
        # At most one list still has nodes, and it is already sorted; attach it whole.
        tail.next = a or b
        return dummy.next

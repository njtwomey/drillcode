"""Merge k Sorted Lists (#23, hard)

Approach: Min-heap of (value, list index, node); pop the smallest and push its successor.
Tricks: The list index in the tuple is a tiebreaker so nodes are never compared;
    pairwise divide-and-conquer merging is the alternative.
Edge cases:
  - Empty lists among the k
  - k = 0
  - All lists empty

Time O(N log k), space O(k).
"""
import heapq


class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        # The heap holds just the current head of each list, so it never exceeds k
        # items and each push/pop costs O(log k). Empty lists are skipped.
        # The index i is a tiebreaker: on equal values, tuples compare i next, so
        # ListNode objects (not orderable) are never compared.
        heap = [(node.val, i, node) for i, node in enumerate(lists) if node]
        heapq.heapify(heap)
        dummy = tail = ListNode()  # dummy avoids special-casing the first node
        while heap:
            _, i, node = heapq.heappop(heap)  # smallest remaining value overall
            tail.next = node
            tail = node
            # Replace the popped node with its successor from the same list.
            if node.next:
                heapq.heappush(heap, (node.next.val, i, node.next))
        return dummy.next

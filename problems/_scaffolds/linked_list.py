class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Node:
    """Node of the Copy List with Random Pointer problem."""

    def __init__(self, x=0, next=None, random=None):
        self.val = int(x)
        self.next = next
        self.random = random


def build_list(array, pos=-1):
    """Build a singly linked list; if pos >= 0 the tail points back to node pos."""
    head = tail = None
    nodes = []
    for val in array:
        node = ListNode(val)
        nodes.append(node)
        if tail is None:
            head = node
        else:
            tail.next = node
        tail = node
    if tail is not None and pos >= 0:
        tail.next = nodes[pos]
    return head


def list_to_array(head):
    array = []
    seen = set()
    while head is not None and id(head) not in seen:
        seen.add(id(head))
        array.append(head.val)
        head = head.next
    return array


def build_random_list(pairs):
    """pairs is [[val, random_index_or_null], ...]."""
    nodes = [Node(val) for val, _ in pairs]
    for i, (_, random_index) in enumerate(pairs):
        if i + 1 < len(nodes):
            nodes[i].next = nodes[i + 1]
        if random_index is not None:
            nodes[i].random = nodes[random_index]
    return nodes[0] if nodes else None


def random_list_to_array(head):
    index = {}
    node = head
    while node is not None and id(node) not in index:
        index[id(node)] = len(index)
        node = node.next
    pairs = []
    node = head
    while node is not None and len(pairs) < len(index):
        random_index = None if node.random is None else index.get(id(node.random))
        pairs.append([node.val, random_index])
        node = node.next
    return pairs

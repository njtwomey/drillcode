Implement a FIFO queue `MyQueue` using only standard stack operations (push to top, pop from top, peek at top, size, is-empty). No other queue or deque structure is allowed.

- `MyQueue()`: creates an empty queue.
- `push(x)`: appends `x` to the back of the queue; returns nothing.
- `pop()`: removes and returns the element at the front.
- `peek()`: returns the front element without removing it.
- `empty()`: returns `True` if the queue holds no elements, else `False`.

Constraints:

- `pop` and `peek` are only called on a non-empty queue
- Up to 100 calls in total
- Amortized O(1) per operation is achievable

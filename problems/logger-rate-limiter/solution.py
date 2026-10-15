"""Logger Rate Limiter (#359, easy)

Approach: A dict from message to the earliest timestamp it may print again.
Tricks: Only update the deadline when a message is printed; a rejected attempt must not
    extend the wait.
Edge cases:
  - Exactly 10 seconds later is allowed
  - Rejected attempts do not push the deadline
  - Same timestamp for the same message

Time O(1) per call, space O(unique messages).
"""

class Logger:
    def __init__(self):
        self.next_allowed = {}  # message -> earliest timestamp it may print again

    def shouldPrintMessage(self, timestamp: int, message: str) -> bool:
        if timestamp < self.next_allowed.get(message, 0):
            return False  # blocked; leave the deadline alone so it is not extended
        self.next_allowed[message] = timestamp + 10
        return True

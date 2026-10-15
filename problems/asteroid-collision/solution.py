"""Asteroid Collision (#735, medium)

Approach: Keep a stack of survivors; a negative asteroid fights the positive tops while
    they are smaller, then dies, ties or is pushed.
Tricks: Only a positive on the stack meeting an incoming negative can collide, and the
    incoming asteroid may destroy several in a row.
Edge cases:
  - Equal sizes destroy each other
  - One asteroid clears several right-movers
  - Left-movers before right-movers never collide
  - Everything cancels out (empty result)

Time O(n), space O(n).
"""

class Solution:
    def asteroidCollision(self, asteroids: List[int]) -> List[int]:
        # The stack holds the asteroids that survive so far, in order. Only a right-mover
        # (positive) followed by a left-mover (negative) can ever collide, so that is the
        # only pairing we must resolve; every other combination just coexists.
        stack = []
        for asteroid in asteroids:
            alive = True
            while alive and asteroid < 0 and stack and stack[-1] > 0:
                top = stack[-1]
                if top < -asteroid:
                    stack.pop()  # the right-mover explodes; the newcomer keeps going
                elif top == -asteroid:
                    stack.pop()  # both explode
                    alive = False
                else:
                    alive = False  # the newcomer explodes
            if alive:
                stack.append(asteroid)
        return stack

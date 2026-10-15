## The idea

The array holds `n + 1` numbers, each between 1 and `n`, so at least one value repeats. The tasks usually forbid changing the array and extra memory, which rules out sorting and sets.

The trick is to read the array as a linked list: from index `i`, the "next" node is `nums[i]`. Every value is at least 1, so nothing ever points at index 0, which makes 0 a safe starting node. Because some value occurs twice, two different indices point at the same node. A list where two nodes share a successor must contain a cycle, and the shared node is where the cycle begins. That node's index is the duplicate value.

## Set-up

- `slow` takes one step per round, `fast` takes two. Both start at `nums[0]`, one step from the head.
- Phase one runs until they meet somewhere inside the cycle.
- Phase two restarts `slow` at the head and moves both at the same speed until they meet again, which is at the cycle entrance.

```text
nums = [1, 3, 4, 2, 2]
index    0  1  2  3  4

As a list:  0 ──▶ 1 ──▶ 3 ──▶ 2 ──▶ 4
                               ▲     │
                               └─────┘
```

The cycle is `2 -> 4 -> 2`, entered at node 2.

## Step by step

Phase one: `slow = nums[slow]`, `fast = nums[nums[fast]]`.

```text
start    slow = nums[0] = 1    fast = 1
round 1  slow = nums[1] = 3    fast = nums[nums[1]] = nums[3] = 2
round 2  slow = nums[3] = 2    fast = nums[nums[2]] = nums[4] = 2
         slow == fast == 2: they met, break.
```

Phase two: put `slow` back at the head and move both one step at a time.

```text
reset    slow = nums[0] = 1    fast = 2
round 1  slow = nums[1] = 3    fast = nums[2] = 4
round 2  slow = nums[3] = 2    fast = nums[4] = 2
         slow == fast == 2: return 2
```

## Why it works

Say the tail before the cycle has length `a`, the meeting point is `b` steps into the cycle, and the cycle has length `c`. When they meet, `slow` has travelled `a + b` and `fast` has travelled twice that. The extra distance `a + b` is a whole number of laps, so `a + b` is a multiple of `c`. That means walking `a` more steps from the meeting point lands exactly on the entrance. A second walker walking `a` steps from the head also lands on the entrance. So moving both one step at a time makes them meet there.

The entrance is the first node with two arrows pointing in, and that is the repeated value.

## Where it goes wrong

Returning the meeting point from phase one. It is somewhere inside the cycle, not necessarily the entrance (in this example it happens to be, which is why the second phase is easy to forget). On `[2, 5, 9, 6, 9, 3, 8, 9, 7, 1]` phase one meets at 7 but the duplicate is 9.

Starting the walk at index 0 is deliberate: nothing points at 0, so it is always on the tail and never inside the cycle.

## Cost

Time O(n): each phase walks at most a couple of passes over the nodes. Space O(1): two indices, and the array is not modified.

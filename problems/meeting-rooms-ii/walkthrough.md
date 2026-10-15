## The idea

The number of rooms needed is the largest number of meetings running at the same moment. We can find that by handling meetings in start order and remembering when each room becomes free. When a new meeting starts, the room that frees up soonest is the only one worth reusing: if even that one is still busy, every room is, and we must open a new one.

A min-heap keeps the earliest end time at the top for cheap access.

## Set-up

- `intervals` is sorted by start time, so each meeting is considered at the moment it begins.
- `ends` is a min-heap of end times, one per room currently in use. `ends[0]` is the earliest.
- `best` is the largest `len(ends)` seen, which is the answer.

## Step by step

`intervals = [[0,30],[5,10],[15,20],[10,25]]`. Sorted: `[0,30], [5,10], [10,25], [15,20]`.

```text
meeting [0,30]   ends is empty                  push 30
                 ends = [30]                    rooms 1   best 1

meeting [5,10]   ends[0] = 30 <= 5 ? no         push 10
                 ends = [10, 30]                rooms 2   best 2

meeting [10,25]  ends[0] = 10 <= 10 ? yes       heapreplace: pop 10, push 25
                 ends = [25, 30]                rooms 2   best 2
                 (touching at 10 is fine, so the room is reused)

meeting [15,20]  ends[0] = 25 <= 15 ? no        push 20
                 ends = [20, 30, 25]            rooms 3   best 3
```

The answer is 3. At time 15 meetings `[0,30]`, `[10,25]` and `[15,20]` are all running. The heap array `[20, 30, 25]` is stored in heap order, not sorted order; only the first entry is guaranteed to be the smallest.

```text
time    0    5    10   15   20   25   30
0-30    |=============================|
5-10         |====|
10-25             |==============|
15-20                  |====|
at 15:  three bars cross the line -> 3 rooms
```

## Why it works

Sorted by start, the earliest-ending busy room is the best candidate to reuse. If its end is `<=` the new start, reuse it. Otherwise all rooms are busy at that start, and the new meeting overlaps all of them, so one more room is truly required. The heap size is then exactly the count of rooms that were needed at the busiest point so far.

## Where it goes wrong

- Using `<` instead of `<=` would treat back-to-back meetings as overlapping and over-count rooms.
- Sorting by end time instead of start time breaks the reasoning that every later meeting starts no earlier than the current one.

## Other approaches

`minMeetingRoomsSweep` sorts the starts and ends separately and walks through the starts with a pointer `j` into the ends. If a start is at or after `ends[j]`, some meeting has finished, so the count stays the same and `j` advances. Otherwise `rooms` goes up. Only the count of open meetings matters, not which meeting is which, so the lists can be sorted independently. It avoids the heap and uses simple arrays.

## Cost

Time O(n log n) for sorting and heap operations. Space O(n) for the heap in the worst case, where every meeting overlaps.

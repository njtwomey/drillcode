## The idea

Every ticket is an edge, and the itinerary must use each edge exactly once. That is an Eulerian path. The twist is the tie-break: among valid itineraries, return the lexically smallest.

Simply taking the smallest next airport can get stuck. Take a smaller airport that has no tickets out, and you strand the rest of the trip. Hierholzer's algorithm handles this without backtracking: follow tickets greedily, smallest first, and when you reach an airport with nothing left, write it down. Airports are written in the order they get stuck, which is the reverse of the real itinerary. Reverse at the end.

A dead end can only be the last stop. Writing it first puts it last after the reversal.

## Set-up

- `graph` maps each airport to its remaining destinations, sorted in reverse so `pop()` from the end returns the smallest. Invariant: each ticket is popped once.
- `route` collects airports in post-order, meaning an airport is appended after all its tickets are used.

Tickets `JFK-AAA, JFK-BBB, BBB-CCC, CCC-JFK` give:

```text
graph = { JFK: [BBB, AAA],     pop() gives AAA first
          BBB: [CCC],
          CCC: [JFK] }
route = []
```

## Step by step

The call tree below shows each `visit` and what is appended.

```text
visit JFK                  pop AAA
  visit AAA                no tickets left from AAA
  append AAA               route = [AAA]
                           back in JFK: pop BBB
  visit BBB                pop CCC
    visit CCC              pop JFK
      visit JFK            no tickets left (JFK list is empty)
      append JFK           route = [AAA, JFK]
    append CCC             route = [AAA, JFK, CCC]
  append BBB               route = [AAA, JFK, CCC, BBB]
append JFK                 route = [AAA, JFK, CCC, BBB, JFK]
```

Reverse it:

```text
route[::-1] = [JFK, BBB, CCC, JFK, AAA]
```

The smallest option AAA was a dead end, so it was written first and ended up last. The loop from JFK through BBB and CCC came back to JFK, and AAA finished the trip.

## Why it works

When `visit` is stuck at an airport, every ticket out of it has been used. Appending it then means everything appended later comes earlier in the final trip. Any side loop that was detoured into returns to the same airport, so it is spliced into the right place. Taking the smallest ticket first at each airport gives the lexical minimum among the valid orders.

## Where it goes wrong

Appending the airport before looping over its tickets, or skipping the reversal, gives the wrong order.

```text
greedy without the dead-end rule:  JFK -> AAA   stuck, tickets left over
```

Duplicate tickets are fine: each is a separate entry in the list and is popped on its own.

## Cost

Sorting the tickets is O(E log E). Each ticket is popped once, so the search is O(E). Space is O(E), including the recursion depth, which can reach E.

## The idea

The majority element appears more than half the time. Imagine every element voting for itself, and pair off each vote with a vote for a different value so that both cancel. Since the majority has more votes than everything else combined, it still has some left after all cancelling. Boyer-Moore voting does this cancelling on the fly with just a candidate and a count.

## Set-up

- `candidate` is the value currently believed to be the majority.
- `count` is how many votes `candidate` has left after cancellation.

Invariant: the elements read so far can be split into pairs of different values, plus `count` extra copies of `candidate`. A majority of the whole list can never be fully paired off, so it ends up as `candidate`.

```text
nums:  2  2  1  1  1  2  2
       ^
candidate = 0, count = 0
```

## Step by step

When `count` is 0, take the current number as the new candidate. Then add 1 for a match, subtract 1 for a mismatch.

```text
num   count==0?  candidate  count
 2     yes          2         1
 2     no           2         2
 1     no           2         1
 1     no           2         0
 1     yes          1         1
 2     no           1         0
 2     yes          2         1
```

The answer is `candidate = 2`. Notice the candidate switched to 1 in the middle, then back to 2, but the true majority (four 2s out of seven) survives to the end.

## Why it works

Each decrement removes one copy of the candidate along with one non-candidate. Those two are a pair of different values, and cancelling a pair of different values cannot remove the majority's lead (it loses at most one of its own for each other element removed). After all the pairs are removed, whatever remains must belong to the majority.

## Where it goes wrong

This only works because the problem promises a majority element exists. On `[1, 2, 3]` the code returns 3, but nothing is a majority; a second pass counting `candidate` would be needed if the guarantee were absent.

```text
nums [1, 2, 3]:  cand 1 (c=1) -> c=0 -> cand 3 (c=1)
returns 3, which is not a majority
```

The order inside the loop matters too: the reset to a new candidate happens before the vote is counted, so the new candidate's own vote makes `count` 1.

## Other approaches

A hash map of counts is O(n) time and O(n) space. Sorting and taking the middle element works because the majority covers more than half the positions, at O(n log n).

## Cost

Time O(n), one pass. Space O(1), two variables.

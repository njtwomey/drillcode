## The idea

The same task cannot run again until `n` other slots have passed. Simulating a scheduler is possible, but there is a closed form, because the most frequent task decides the whole shape of the schedule.

Say the busiest task `A` runs `most` times. Between two copies of `A` there must be at least `n` other slots. So the schedule looks like `most - 1` frames of length `n + 1` (one `A` plus `n` slots for anything else) followed by a last partial row. Everything else fits into the gaps. Only the length of that frame skeleton matters. If there are so many tasks that the gaps overflow, nothing idles and the answer is just the number of tasks.

## Set-up

- `counts` is the frequency of each task type.
- `most` is the highest frequency.
- `tied` is how many types share that highest frequency. They all need a slot in the last row.
- `frames = (most - 1) * (n + 1) + tied` is the length of the skeleton.
- Final answer: `max(len(tasks), frames)`.

## Step by step

Tasks `A A A B B C`, `n = 2`. Counts are A:3, B:2, C:1, so `most = 3`, `tied = 1`.

```text
frames = (3 - 1) * (2 + 1) + 1 = 7

  frame 1     frame 2     last row
 [A  B  C ] [A  B  _ ] [A]
  1  2  3     4  5  6    7

Fill the busiest task first, then drop B and C into the gaps.
Slot 6 is idle. 6 tasks, 7 slots: answer max(6, 7) = 7.
```

With a tie, `A A A B B B` and `n = 2`, `most = 3`, `tied = 2`:

```text
frames = 2 * 3 + 2 = 8

 [A  B  _ ] [A  B  _ ] [A  B]
  1  2  3     4  5  6    7  8
```

Two idle slots, answer 8. The last row holds one copy of each tied task, which is why `tied` is added.

## Why it works

The skeleton is a lower bound: `A` needs `most - 1` full cooldown gaps, and each tied task must also appear in the final row. It is also achievable, since the other tasks have lower or equal counts and can be spread into the frames without breaking any cooldown. When tasks outnumber the skeleton, the extra ones can lengthen the frames without idling, so the answer is exactly `len(tasks)`.

```text
tasks A A A B B B C C C D D D, n = 2
frames = 2 * 3 + 4 = 10 < 12 tasks, so answer = 12 (no idle slot needed)
```

## Where it goes wrong

- Forgetting `tied`. For `A A A B B B` it gives `2 * 3 = 6`, short of the true 8.
- Forgetting the `max` with `len(tasks)`. If many task types exist, the formula gives a number below the task count, which cannot be right.
- Using `n` where `n + 1` belongs. A frame holds the task itself plus its `n` cooldown slots.

With `n = 0` the frame length is 1 and the formula gives `most - 1 + tied`, which never exceeds `len(tasks)`, so the `max` returns the task count.

## Cost

Time O(T) to count the tasks `T`, plus O(1) for the formula (task types are bounded by 26). Space O(1): at most 26 counters.

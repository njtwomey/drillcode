## The idea

For each message we only need one fact: the earliest time it may print again. If the message printed at time `t`, that time is `t + 10`. A call is allowed when its timestamp has reached the stored deadline.

A dictionary from message to deadline does it. There is no need to keep every past timestamp or clean anything up on a schedule.

## Set-up

- `self.next_allowed` maps a message to the earliest timestamp it may print again. A message that has never printed is missing, and `.get(message, 0)` treats that as a deadline of 0, which any timestamp meets.

```text
next_allowed = {}
```

## Step by step

```text
call               deadline   decision                  next_allowed
(1,  foo)          0          1 >= 0   print            {foo: 11}
(2,  bar)          0          2 >= 0   print            {foo: 11, bar: 12}
(3,  foo)          11         3 < 11   blocked          unchanged
(8,  bar)          12         8 < 12   blocked          unchanged
(10, foo)          11         10 < 11  blocked          unchanged
(11, foo)          11         11 >= 11 print            {foo: 21, bar: 12}
```

Output: true, true, false, false, false, true. Note the last call is exactly 10 seconds after the first `foo`, and it is allowed.

## Why it works

The deadline for a message is always "time of its last printed copy + 10". A new call is allowed exactly when its timestamp is not before that, and then it becomes the last printed copy, so the deadline moves forward. Calls arrive in non-decreasing time, so a stored deadline is never wrongly compared against an earlier clock.

## Where it goes wrong

Updating the deadline on a rejected call pushes the wait forward and punishes the caller for trying.

```text
(1, a) printed -> deadline 11
(5, a) blocked, but if we wrote 5 + 10 = 15 ...
(11, a) now blocked too: wrong, it should print
```

The check also has to be `<`, not `<=`. At timestamp 10 after a print at 0, the message is allowed again.

## Cost

Each call is one dictionary lookup and maybe one write: O(1). Space is O(number of distinct messages).

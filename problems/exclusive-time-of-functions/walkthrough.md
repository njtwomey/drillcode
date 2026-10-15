## The idea

A function that calls another one is paused while the callee runs. So the logs behave like parentheses: every `end` closes the most recent unclosed `start`. That is a stack.

The trick for the arithmetic is to be lazy. When a call ends, add its whole span (including its callees) to its own total. Then subtract that same span from the caller, who was not running during it. Callees get charged to themselves and removed from their parent, so each time unit ends up counted for exactly one function.

## Set-up

- `result` is one total per function id, all zero. A function never logged stays at `0`.
- `stack` holds `(function id, start time)` for every call that has started and not ended. The top is the call currently running. Each call is its own entry, which is why recursion needs no special handling.
- An `end` stamp is inclusive: the function runs during that whole unit. So a span is `stamp - start + 1`.

```text
logs: 0:start:0  1:start:2  1:end:5  0:end:6

stack   (empty)
result  [0, 0]
```

## Step by step

```text
0:start:0     push (0, 0)
              stack: (0,0)                       result [0, 0]

1:start:2     push (1, 2)
              stack: (0,0) (1,2)                 result [0, 0]

1:end:5       pop (1, 2).  span = 5 - 2 + 1 = 4
              result[1] += 4
              caller is id 0: result[0] -= 4
              stack: (0,0)                       result [-4, 4]

0:end:6       pop (0, 0).  span = 6 - 0 + 1 = 7
              result[0] += 7
              stack empty, nobody to subtract from
              stack: (empty)                     result [3, 4]
```

Function 0 ran at times 0, 1 and 6 (three units); function 1 ran at 2 to 5 (four units). The answer `[3, 4]` matches.

## Why it works

A call's span covers its own running time plus all time spent in nested calls. Each direct child already subtracted its own span from this call when it ended, so by the time this call ends, the total is its span minus its children's spans, which is its exclusive time. Grandchildren are handled by the children, who have subtracted theirs. The numbers can dip below zero in between (like the `-4` above) and settle at the end.

## Where it goes wrong

- Using `stamp - start` instead of `stamp - start + 1`. With `0:start:0, 0:end:0` the function ran for one unit, not zero.
- Keying a dictionary on the function id for start times. A recursive function has several live calls with the same id, so you need a stack entry per call.
- Subtracting from the caller when the stack is empty. The `if stack` check covers the outermost call.

## Cost

Time O(L) for `L` log lines: each is parsed and either pushed or popped once. Space O(L) in the worst case, when calls nest as deep as the log.

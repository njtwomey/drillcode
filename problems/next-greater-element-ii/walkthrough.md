## The idea

For each element we want the first strictly larger value that follows it when the array is treated as a circle. Scanning forward from every index is O(n^2). A stack does it in one sweep: keep the indices that are still waiting for a bigger value, and when a bigger value shows up, it answers every waiting index it beats.

The circle is handled by walking the array twice. Index `i` in the range `0..2n-1` reads `nums[i % n]`, so the second pass lets the early elements "see" the ones before them.

## Set-up

- `result = [-1] * n`: the default answer, kept for anything never beaten (the maximum and its duplicates).
- `stack` holds indices still waiting. Invariant: their values are non-increasing from bottom to top, so the top is the easiest to beat.
- `value = nums[i % n]` is the number arriving at step `i`.

```text
nums   = [1, 2, 1]
index     0  1  2
result = [-1, -1, -1]
stack  = []        (top on the right)
```

## Step by step

At each `i`: while the top index has a smaller value than `value`, pop it and set `result[popped] = value`. Then, only if `i < n`, push `i`.

```text
i=0  value=1  stack empty
       push 0                         stack=[0]          result=[-1,-1,-1]
i=1  value=2  nums[0]=1 < 2: pop 0
       result[0]=2, push 1            stack=[1]          result=[ 2,-1,-1]
i=2  value=1  nums[1]=2 < 1? no
       push 2                         stack=[1,2]        result=[ 2,-1,-1]
--- second pass: no more pushes ---
i=3  value=nums[0]=1  nums[2]=1 < 1? no
                                      stack=[1,2]
i=4  value=nums[1]=2  nums[2]=1 < 2: pop 2
       result[2]=2                    stack=[1]
       nums[1]=2 < 2? no
i=5  value=nums[2]=1  nums[1]=2 < 1? no
                                      stack=[1]          result=[ 2,-1, 2]
```

Index 1 (the value 2, the maximum) stays on the stack, so its `-1` stands. The last 1 found its answer by wrapping round to the 2.

## Why it works

Each index waits on the stack until the first later value that exceeds it, and that is exactly the next greater element. Values on the stack are non-increasing, so a new value either beats the top or beats nothing: popping stops at the first index it cannot beat. Two passes cover every element's full circle, because any candidate lies within the next `n - 1` positions.

## Where it goes wrong

- Pushing during the second pass. Indices would be added twice, the stack would hold duplicates, and the work would no longer be bounded. Only `i < n` pushes.
- Using `<=` in the pop test. Equal values are not greater, so with `[2, 2, 2]` everything must stay `-1`.
- Resolving with a non-strict comparison would also give the maximum a wrong answer.

```text
nums = [2, 2, 2], using <= by mistake
  i=1 pops index 0 -> result[0] = 2   (wrong, 2 is not greater than 2)
```

## Cost

Time O(n): `2n` steps, and each index is pushed once and popped at most once. Space O(n) for `result` and the stack.

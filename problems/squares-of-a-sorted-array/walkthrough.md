## The idea

Squaring each number is easy, but sorting the results afterwards costs O(n log n), and it ignores that the input was already sorted. The catch is negatives: `-4` squared is 16, which is bigger than `3` squared. Still, the order is not random. The squares are largest at the two ends of the array, because that is where the numbers with the largest magnitude sit (big negatives on the left, big positives on the right), and they shrink towards the middle.

So build the answer from the largest square downward. At each step the biggest remaining square is at one of the two ends, and we can pick it with two pointers.

## Set-up

- `result` is a list of `len(nums)` zeros, filled from the back.
- `left` and `right` point at the two ends of the unconsumed part of `nums`.
- `i` is the slot being filled, counting down from the last index.

Invariant: `result[i + 1:]` already holds the largest squares in ascending order, and every unused number is between `left` and `right`.

```text
nums   = [-4, -1,  0,  3, 10]
           ^                ^
         left             right
result = [ 0,  0,  0,  0,  0]
                           ^ i = 4
```

## Step by step

Each round compares `abs(nums[left])` with `abs(nums[right])`, writes the larger one's square at `i`, and moves that pointer inwards.

```text
nums = [-4, -1, 0, 3, 10]

i=4  left=0 right=4   |-4|=4 vs |10|=10   right wins
     result[4] = 100                       result = [0, 0, 0, 0, 100]

i=3  left=0 right=3   |-4|=4 vs |3|=3      left wins
     result[3] = 16                        result = [0, 0, 0, 16, 100]

i=2  left=1 right=3   |-1|=1 vs |3|=3      right wins
     result[2] = 9                         result = [0, 0, 9, 16, 100]

i=1  left=1 right=2   |-1|=1 vs |0|=0      left wins
     result[1] = 1                         result = [0, 1, 9, 16, 100]

i=0  left=2 right=2   |0|=0 vs |0|=0       tie, else branch takes right
     result[0] = 0                         result = [0, 1, 9, 16, 100]
```

The result is already sorted, with no sort call.

## Why it works

The largest square among the unused numbers must come from the one with the largest absolute value. In a sorted array that number is either the leftmost (most negative) or the rightmost (most positive), so comparing those two always finds it. Filling from the back means each pick is the biggest of what is left.

## Where it goes wrong

Filling from the front would need the smallest square, which is in the middle for mixed signs, and that is not at either pointer. Comparing `nums[left]` and `nums[right]` directly instead of their absolute values is the other trap:

```text
nums = [-4, 3]     -4 < 3 would pick 3 first, giving [16, 9]   wrong
by absolute value: 4 > 3 picks -4 first, giving [9, 16]        right
```

On a tie, either side may be taken; the squares are equal.

## Cost

Time O(n): each number is consumed once. Space O(n) for the result list; the two pointers add O(1).

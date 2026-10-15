## The idea

The unsorted version of this problem needs a hash map, because you cannot tell which direction to move after looking at a pair. Here the array is sorted, and that gives every comparison a meaning. Look at the smallest and the largest remaining numbers. If their sum is too small, the smallest one can never be part of the answer, since even the biggest partner is not enough. If the sum is too big, the largest one is ruled out the same way. Either way one number is discarded per step, and you never need to try all pairs.

## Set-up

- `left` starts at index 0, the smallest value.
- `right` starts at the last index, the largest value.
- `total` is the sum of the two values under the pointers.

The invariant: if a valid pair exists, both of its indexes lie inside `[left, right]`. We only ever move a pointer past a number we have proved cannot be in any answer.

```text
numbers = [1, 3, 5, 8, 11]     target = 13

index:     0  1  2  3  4
value:     1  3  5  8  11
           ^           ^
           left        right
```

## Step by step

```text
Round 1  1 + 11 = 12  < 13   too small, drop numbers[left]
         [1  3  5  8  11]
          ^           ^
          left=0      right=4          then left += 1

Round 2  3 + 11 = 14  > 13   too big, drop numbers[right]
         [1  3  5  8  11]
             ^        ^
             left=1   right=4          then right -= 1

Round 3  3 + 8  = 11  < 13   too small, drop numbers[left]
         [1  3  5  8  11]
             ^     ^
             left=1  right=3           then left += 1

Round 4  5 + 8  = 13  == 13  found
         [1  3  5  8  11]
                ^  ^
                left=2 right=3
```

The code returns `[left + 1, right + 1]` = `[3, 4]`. The problem asks for 1-indexed positions, hence the `+ 1`.

## Why it works

Suppose `numbers[left] + numbers[right] < target`. For any index `k` in range, `numbers[k] <= numbers[right]`, so `numbers[left] + numbers[k] < target` too. That means `numbers[left]` has no partner and can be dropped safely. The mirror argument covers the `>` case. Because each step removes an index that cannot be in the answer, and an answer is guaranteed, the pointers meet it before they cross.

## Where it goes wrong

- Returning 0-indexed positions. The statement wants 1-indexed.
- Using `left <= right`. That would allow pairing a number with itself. With `[3, 3]` and target 6 the pointers are at different indexes, so duplicates are fine, but the same index must never be used twice.
- Moving the wrong pointer. If the sum is too small, only increasing `left` can raise it.

## Cost

Time O(n): each step moves one pointer inward, so at most n - 1 steps. Space O(1): two integers. A hash map would also be O(n) time but O(n) space, and binary searching each partner would cost O(n log n).

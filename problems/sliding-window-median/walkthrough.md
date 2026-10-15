## The idea

The median is the middle of the sorted window. If the window is kept sorted, the median is just one or two index lookups. Sliding by one means one value leaves and one value enters, and a sorted list can handle both with a binary search.

The textbook alternative is two heaps with lazy deletion, which is fiddly to get right. A plain sorted Python list is far simpler. Finding the spot is O(log k), and the shift of elements is a fast memory move, so in practice it is quick.

## Set-up

- `window = sorted(nums[:k])` is the first window, sorted.
- `mid = k // 2` is the middle position. For odd `k` the median is `window[mid]`. For even `k` it is the average of `window[mid - 1]` and `window[mid]`.
- `result` collects the medians.

The invariant: at the top of each loop `window` holds exactly the sorted values of `nums[i - k : i]`.

```text
nums = [1, 3, -1, -3, 5, 3, 6, 7]     k = 3     mid = 1

window = sorted([1, 3, -1]) = [-1, 1, 3]
          index              0   1  2
                                 ^ mid
```

## Step by step

Per round: record the median, then (unless it was the final window) remove `nums[i - k]` with `del window[bisect_left(...)]` and add `nums[i]` with `insort`.

```text
window [-1, 1, 3]   median 1
   remove 1, add -3        [-3, -1, 3]    median -1
   remove 3, add 5         [-3, -1, 5]    median -1
   remove -1, add 3        [-3, 3, 5]     median 3
   remove -3, add 6        [3, 5, 6]      median 5
   remove 5, add 7         [3, 6, 7]      median 6

result = [1, -1, -1, 3, 5, 6]
```

The loop runs `i` from `k` to `len(nums)` inclusive. The last iteration records the final median and breaks before sliding, because there is no `nums[len(nums)]` to add.

## Why it works

`bisect_left` finds the first position holding the outgoing value, and that value is definitely in the window, so deleting at that index removes exactly one copy. `insort` puts the new value in its sorted place. After both, the list is the sorted new window.

## Where it goes wrong

- Using `//` for even `k` truncates the half. The code uses `/` so `[1, 2]` gives `1.5`.
- Deleting by value with a linear `remove` also works but is slower to find.
- Slicing and re-sorting each window is O(n * k log k).

## Cost

Time O(n * k) worst case: each slide does an O(log k) search plus an O(k) shift of the list (done in fast native code). Space O(k) for `window`.

## Other approaches

Two heaps (a max-heap for the lower half and a min-heap for the upper half) with lazy deletion gives O(n log k), but needs careful bookkeeping of sizes and stale entries.

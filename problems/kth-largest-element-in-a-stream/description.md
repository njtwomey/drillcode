Design a class `KthLargest` that tracks the kth largest element of a stream of integers. Here "kth largest" means the kth in sorted order, so duplicates count separately.

`KthLargest(k, nums)` initialises the object with the integer `k` and the starting stream `nums`, which may be shorter than `k`. `add(val)` appends `val` to the stream and returns the current kth largest element.

Every call to `add` is made once the stream has at least `k` elements, so there is always an answer to return.

Constraints:
- `1 <= k <= 10^4`
- `0 <= nums.length <= 10^4`
- At most `10^4` calls to `add`

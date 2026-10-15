## The idea

Building a permutation is a series of choices: pick the first element, then the second from what remains, and so on. Every complete sequence of choices is one answer. That is a decision tree, and depth-first search walks all of it.

The trick is to use one shared `path` that grows and shrinks as the search goes down and back up, rather than building a new list at every step. Going back up means undoing the last choice (backtracking).

## Set-up

- `result` collects finished permutations.
- `path` is the permutation being built. It is shared, so it is mutated in place.
- `used[i]` says whether `nums[i]` is already in `path`.

The invariant: at any call, `path` holds the choices made on the way down, and `used` marks exactly those elements.

```text
nums = [1, 2, 3]
path = []        used = [F, F, F]
```

## Step by step

At every call the loop starts from index 0 and skips used entries. That is why all orderings appear: position 1 can try 1, 2 or 3, and later positions can reach elements before the one chosen earlier. Here is the search under the first choice. The call that adds an element is shown with its resulting `path`.

```text
path []
├─ choose 1   path [1]    used [T,F,F]
│  ├─ choose 2   path [1,2]     used [T,T,F]
│  │  └─ choose 3   path [1,2,3]  full -> save copy
│  │     (pop 3, back to [1,2])
│  │  (pop 2, back to [1])
│  └─ choose 3   path [1,3]     used [T,F,T]
│     └─ choose 2   path [1,3,2]  full -> save copy
├─ choose 2   ... gives [2,1,3] and [2,3,1]
└─ choose 3   ... gives [3,1,2] and [3,2,1]
```

Order saved: 123, 132, 213, 231, 312, 321.

## Why it works

Each level of the tree fixes one position, and the unused elements are exactly the options for the next position. Every leaf is a distinct full ordering, and every ordering is a leaf, so nothing is missed or repeated. Undoing both `path.pop()` and `used[i] = False` returns the state to what it was, so the next sibling branch starts clean.

## Where it goes wrong

- Appending `path` itself instead of `path[:]`. Later pops would empty the stored lists.

```text
result.append(path)     after the search:  [[], [], [], [], [], []]
result.append(path[:])  after the search:  [[1,2,3], [1,3,2], ...]
```

- Forgetting to reset `used[i]` after the recursive call, which blocks all later branches from using that element.
- Starting the loop from a start index (like combinations do): that would only yield increasing sequences.

## Cost

There are n! permutations and each is copied in O(n), so time is O(n * n!). Extra space apart from the output is O(n): the path, `used` and the recursion depth.

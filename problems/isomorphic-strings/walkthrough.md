## The idea

Two strings are isomorphic if you can rename characters in `s` to get `t`, with the rule that the renaming is a consistent one-to-one pairing: the same letter always becomes the same letter, and two different letters never become the same one. So `egg` and `add` match (e to a, g to d), but `badc` and `baba` do not (b and d would both become b).

Checking only "same source gives same target" misses the second half. That needs a map in the opposite direction too.

## Set-up

- `s_to_t` records what each character of `s` has been paired with.
- `t_to_s` records the reverse: what each character of `t` came from.

Invariant: after processing a prefix, the two dicts are exact inverses of each other, and every pair seen so far respects both.

## Step by step

For `s = "egg"`, `t = "add"`:

```text
pair    s_to_t.get(a, b) != b ?   t_to_s.get(b, a) != a ?   after
e, a    (default a) ok            (default e) ok            e->a   a->e
g, d    (default d) ok            (default g) ok            g->d   d->g
g, d    d == d ok                 g == g ok                 unchanged
return True
```

Now `s = "badc"`, `t = "baba"`, the failing case:

```text
s_to_t        t_to_s
b -> b        b -> b          after (b, b)
a -> a        a -> a          after (a, a)
(d, b): s_to_t has no d, so default b == b passes,
        but t_to_s['b'] is 'b', not 'd', so the second test fails.
return False
```

The forward map alone would have accepted `d -> b`. It is the reverse map that notices `b` already belongs to `b`.

## Why it works

Each new pair `(a, b)` is checked against both dicts. If either already holds a different partner for `a` or for `b`, the pairing cannot be a one-to-one function, so the answer is no. If we get through every position, all pairs agree with a single bijection.

## Where it goes wrong

Using one dict, or storing only after a check against one side. Also watch the length: `zip` stops at the shorter string. LeetCode guarantees equal lengths here, so no extra check is needed, but with unequal inputs you would have to compare lengths first.

A character that maps to itself is fine (`b -> b` above). It is not a conflict.

## Cost

Time O(n), one pass with constant-time dict operations. Space O(1) in the sense of bounded alphabet (at most 256 characters in each dict); in general O(k) for k distinct characters.

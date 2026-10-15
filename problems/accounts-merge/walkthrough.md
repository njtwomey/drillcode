## The idea

Two accounts belong to the same person when they share at least one email, and that link is transitive: A shares with B, B shares with C, so all three are one person. The name is not a reliable key, since two different people can have the same name.

This is a "which things are connected?" problem, which is what union-find (a disjoint-set structure) is for. The trick is to union the emails, not the accounts. An email is the real identity. Join all the emails of one account together, and any email that appears in two accounts automatically links them.

## Set-up

- `parent` maps each email to its parent in a union-find forest. A new email starts as its own parent (its own root).
- `owner` maps each email to the account name it was first seen with.
- `find(x)` follows parents up to the root, shortening the path as it goes (path halving).
- `groups` is built at the end: root email to the list of emails under it.

Invariant: two emails have the same root exactly when some chain of accounts links them.

## Step by step

```text
accounts:
  0: John  a  b
  1: John  b  c
  2: Mary  d
  3: John  e
```

Each account unions all its emails with its first email:

```text
Account 0 (John a b):  a is new (own root).  b is new, then
                       parent[find(b)] = find(a)

      a ◀── b           parent: a:a  b:a

Account 1 (John b c):  b already known.  c is new.  Attach to find(b) = a.

      a ◀── b
      ▲                 parent: a:a  b:a  c:a
      └──── c

Account 2 (Mary d):    d:d              (alone)
Account 3 (John e):    e:e              (alone)
```

Account 1 is merged into account 0 purely because they share `b`. Grouping by root:

```text
find(a)=a  find(b)=a  find(c)=a   ->  a: [a, b, c]
find(d)=d                         ->  d: [d]
find(e)=e                         ->  e: [e]

output: [John a b c]   [Mary d]   [John e]
```

Each group is the owner's name from the root email, followed by the sorted emails. The two Johns stay apart because they share no email.

## Why it works

Union-find keeps one root per connected set, and every union records a real fact: "these emails are in the same account". Transitive merges come for free, since joining sets is symmetric and chains collapse onto a single root. Grouping by root then reads the connected sets back.

## Where it goes wrong

Merging by name would wrongly join the two Johns above. Keying unions by account index also needs extra bookkeeping to detect shared emails. Also note the name lookup happens after grouping, from the root; every email in a group has the same owner name by construction, so any of them would do.

An email repeated within one account is harmless: `email not in parent` is false the second time and the union is a no-op.

## Cost

With N total emails: time O(N log N * α(N)), dominated by sorting each group, with near-constant union-find work (α is the inverse Ackermann function). Space O(N) for `parent`, `owner` and `groups`.

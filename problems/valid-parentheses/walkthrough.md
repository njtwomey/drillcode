## The idea

In a valid string, every closing bracket closes the most recently opened bracket that is still open. "Most recent first" is exactly how a stack behaves. So push each opener, and when a closer arrives, it must match whatever is on top.

Counting brackets of each kind is not enough, because `"([)]"` has balanced counts but the pairs cross over each other. The stack captures the nesting order.

## Set-up

- `pairs` maps each closer to its opener: `)` to `(`, and so on. It is keyed by closer so that `ch in pairs` also tells us whether `ch` is a closer.
- `stack` holds the openers that have not been closed yet, oldest at the bottom. Invariant: the stack is the exact list of brackets still waiting for their partner.

```text
s = "{[()]}"

stack: (empty)  ->  scanning from the left
```

## Step by step

```text
read '{'  opener, push        stack: { 
read '['  opener, push        stack: { [
read '('  opener, push        stack: { [ (
read ')'  closer. pop '(' ; pairs[')'] is '(' -> match
                              stack: { [
read ']'  closer. pop '[' ; pairs[']'] is '[' -> match
                              stack: {
read '}'  closer. pop '{' ; pairs['}'] is '{' -> match
                              stack: (empty)
```

The stack is empty at the end, so the result is `True`.

A failing case, `"([)]"`:

```text
read '('  push                stack: (
read '['  push                stack: ( [
read ')'  closer. pop '[' ; pairs[')'] is '(' -> mismatch -> False
```

## Why it works

When a closer arrives, the only bracket it is allowed to close is the innermost open one, which is the top of the stack. If the top is something else, no later character can repair that, so returning `False` is safe. If every closer finds its partner and nothing is left over, each opener was closed in the right order.

## Where it goes wrong

Two checks are easy to forget:

- A closer with an empty stack, such as `")"`. The `not stack` test returns `False` before `pop()` would crash on an empty list.
- Leftover openers at the end, such as `"(("`. Every closer matched, but the stack is not empty, so `return not stack` gives `False`.

```text
s = "(("      push, push     stack: ( (    -> not empty -> False
s = ")"       closer, stack is empty      -> False
```

## Cost

Time O(n): one pass with constant-time push, pop and lookup. Space O(n): in the worst case, such as a string of only openers, the stack holds everything.

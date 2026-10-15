## The idea

The news feed is a merge of several already-sorted lists: your own tweets and those of everyone you follow, each ordered by time. You want the 10 newest across all of them. Gathering every tweet and sorting would work but touches far more data than needed.

Because each user's list is already in time order, the newest tweet of the whole feed must be the newest tweet of some single user. So keep a max-heap with just one candidate per user: that user's newest tweet not yet used. Pop the best, then push the next-newest from the same user. This is the standard k-way merge, and it stops after 10 pops.

## Set-up

- `self.time` is a global counter that goes up with every `postTweet`. Tweet ids are not ordered by posting, so the counter is what defines "newest".
- `self.tweets[user]` is a list of `(time, tweetId)`, oldest first, so the newest is at the end.
- `self.following[user]` is the set of people they follow. `follow` adds, `unfollow` uses `discard`, so removing someone you never followed is harmless.
- Inside `getNewsFeed`, `heap` holds `(-time, tweetId, user, idx)`. Python's heap is a min-heap, so negating the time makes the newest tweet come out first. `idx` says which tweet of that user's list it is.

```text
post(1, 5)  post(2, 6)  post(1, 7)   follow(1, 2)

tweets[1] = [(1, 5), (3, 7)]
tweets[2] = [(2, 6)]
following[1] = {2}
```

## Step by step

`getNewsFeed(1)`: the users are `{2} | {1}`. Push each user's newest tweet.

```text
heap start (shown as time, tweet, user, idx):
   (t3, 7, user 1, idx 1)
   (t2, 6, user 2, idx 0)

pop t3  -> result [7]
   user 1 has idx 0: push (t1, 5, user 1, idx 0)
   heap: (t2, 6, u2)  (t1, 5, u1)

pop t2  -> result [7, 6]
   user 2 has no earlier tweet: push nothing
   heap: (t1, 5, u1)

pop t1  -> result [7, 6, 5]
   user 1 has no earlier tweet: heap empty, stop
```

The feed is `[7, 6, 5]`, newest first.

## Why it works

At any moment the heap holds, for each user, the newest tweet not yet returned. The newest tweet still unreturned across all users has to be one of those, so the top of the heap is correct. After removing it, the only list whose front changed is that user's, so only that user's next tweet is pushed. Repeating it gives tweets in strict time order, and we stop at 10.

## Where it goes wrong

- Ordering by `tweetId` instead of time. The problem says "most recent" means the order of the calls, so use the counter.
- Forgetting that a user always sees their own tweets. The code adds `{userId}` to the followee set, so following yourself or not changes nothing.
- Pushing every tweet of every followee into the heap. That works but costs time proportional to all tweets; pushing one per user keeps the cost low.

```text
user with 1000 tweets, feed needs 10
  push all:    heap gets 1000 entries
  push newest: heap gets 1 entry, grows by 1 per pop
```

## Cost

`postTweet`, `follow` and `unfollow` are O(1). `getNewsFeed` builds a heap of up to `f` entries (one per followee) and does at most 10 pops and pushes, so it costs O(f + 10 log f), written O(f). Space is O(tweets + follows) for the stored data.

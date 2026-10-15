Design a simplified social feed. Users are identified by integer ids and every tweet has a unique integer id.

- `postTweet(userId, tweetId)` publishes a tweet.
- `getNewsFeed(userId)` returns the ids of the 10 most recent tweets in that user's feed, newest first. The feed contains the user's own tweets and those of every user they follow. Fewer than 10 are returned if fewer exist.
- `follow(followerId, followeeId)` makes the first user follow the second.
- `unfollow(followerId, followeeId)` undoes that; it does nothing if the follow does not exist.

"Most recent" is the order in which `postTweet` was called, not the size of the tweet id.

Constraints:
- `1 <= userId, followerId, followeeId <= 500`
- `0 <= tweetId <= 10^4`
- At most `3 * 10^4` calls in total

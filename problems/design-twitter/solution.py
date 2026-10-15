"""Design Twitter (#355, medium)

Approach: Per-user tweet lists stamped with a global counter, merged across followees
    with a max-heap.
Tricks: Each list is already time-ordered, so push only the newest tweet per user and
    advance the list you pop from; stop at 10.
Edge cases:
  - User with no tweets or followees
  - Following yourself or unfollowing someone never followed
  - More than 10 tweets in the feed
  - Newest means latest posted, not largest tweet id

Time O(f) per getNewsFeed (f followees), O(1) otherwise, space O(tweets + follows).
"""

import heapq
from collections import defaultdict


class Twitter:
    def __init__(self):
        self.time = 0  # global counter so tweets from different users can be ordered
        self.tweets = defaultdict(list)  # user -> [(time, tweetId)], oldest first
        self.following = defaultdict(set)  # user -> set of followees

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.time += 1
        self.tweets[userId].append((self.time, tweetId))

    def getNewsFeed(self, userId: int) -> List[int]:
        # Every user's list is already sorted by time, so this is a k-way merge:
        # a max-heap (negated time) holds each user's newest unread tweet.
        users = self.following[userId] | {userId}  # a user always sees their own tweets
        heap = []
        for user in users:
            if self.tweets[user]:
                idx = len(self.tweets[user]) - 1
                time, tweetId = self.tweets[user][idx]
                heap.append((-time, tweetId, user, idx))
        heapq.heapify(heap)

        result = []
        while heap and len(result) < 10:
            _, tweetId, user, idx = heapq.heappop(heap)
            result.append(tweetId)
            if idx > 0:  # advance only the list we just took from
                time, nextId = self.tweets[user][idx - 1]
                heapq.heappush(heap, (-time, nextId, user, idx - 1))
        return result

    def follow(self, followerId: int, followeeId: int) -> None:
        self.following[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        self.following[followerId].discard(followeeId)  # no error if not following

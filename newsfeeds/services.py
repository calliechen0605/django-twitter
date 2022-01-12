from friendships.services import FriendshipService
from newsfeeds.models import NewsFeed

#service一般都是class method, 不需要new instance
class NewsFeedService(object):

    @classmethod
    def fanout_to_followers(cls, tweet):
        followers = FriendshipService.get_followers(tweet.user)
        #production 里不允许for + sql query
       # for follower in followers:
            #NewsFeed.objects.create(user = follower, tweet = tweet)
        newsfeeds = [
            NewsFeed(user = follower, tweet = tweet)
            for follower in followers
        ]
        newsfeeds.append(NewsFeed(user = tweet.user, tweet = tweet))
        NewsFeed.objects.bulk_create(newsfeeds)





from datetime import timedelta
from testing.testcases import TestCase
from tweets.constants import TweetPhotoStatus
from tweets.models import Tweet
from tweets.models import TweetPhoto
from tweets.services import TweetService
from utils.redis_client import RedisClient
from utils.time_helpers import utc_now
from utils.redis_serializers import DjangoModelSerializer
from twitter.cache import USER_TWEETS_PATTERN


class TweetTests(TestCase):

    def setUp(self):
        self.clear_cache()
        self.linghu = self.create_user('linghu')
        self.tweet = self.create_tweet(self.linghu, content='Jiuzhang Dafa Hao')

    def test_hours_to_now(self):
        tweet = Tweet.objects.create(user=self.linghu, content='Callie is an idiot')
        tweet.created_at = utc_now() - timedelta(hours=10)
        tweet.save()
        self.assertEqual(tweet.hours_to_now, 10)

    def test_like_set(self):
        self.create_like(self.linghu, self.tweet)
        self.assertEqual(self.tweet.like_set.count(), 1)

        self.create_like(self.linghu, self.tweet)
        self.assertEqual(self.tweet.like_set.count(), 1)

        dongxie = self.create_user('dongxie', 'dongxie@gmail.com')
        self.create_like(dongxie, self.tweet)
        self.assertEqual(self.tweet.like_set.count(), 2)

    def test_create_photo(self):
        photo = TweetPhoto.objects.create(
            tweet=self.tweet,
            user=self.linghu,
        )
        self.assertEqual(photo.user, self.linghu)
        self.assertEqual(photo.status, TweetPhotoStatus.PENDING)
        self.assertEqual(self.tweet.tweetphoto_set.count(), 1)

    def test_cache_tweet_in_redis(self):
        tweet = self.create_tweet(self.linghu)
        conn = RedisClient.get_connection()
        serialized_data = DjangoModelSerializer.serialize(tweet)
        conn.set(f'tweet:{tweet.id}', serialized_data)
        # 这里test一个不存在的key， key的内容是 tweet : not_exists
        data = conn.get(f'tweet:not_exists')
        self.assertEqual(data, None)

        data = conn.get(f'tweet:{tweet.id}')
        cached_tweet = DjangoModelSerializer.deserialize(data)
        self.assertEqual(tweet, cached_tweet)


class TweetServiceTests(TestCase):

    def setUp(self):
        self.clear_cache()
        self.linghu = self.create_user('linghu')

    def test_get_user_tweets(self):
        tweet_ids = []
        for i in range(3):
            tweet = self.create_tweet(self.linghu, 'tweet {}'.format(i))
            tweet_ids.append(tweet.id)
        # reverse this list
        tweet_ids = tweet_ids[::-1]

        RedisClient.clear()
        conn = RedisClient.get_connection()

        # Try to get it for the first time
        tweets = TweetService.get_cached_tweets(self.linghu.id)
        self.assertEqual([t.id for t in tweets], tweet_ids)

        #Try to get it for the second time
        tweets = TweetService.get_cached_tweets(self.linghu.id)
        self.assertEqual([t.id for t in tweets], tweet_ids)

        #cache update
        new_tweet= self.create_tweet(self.linghu, content="new tweet")
        tweets = TweetService.get_cached_tweets(self.linghu)
        tweet_ids.insert(0, new_tweet.id)
        self.assertEqual([t.id for t in tweets], tweet_ids)

    def test_create_new_tweet_before_get_cached_tweets(self):
        tweet1 = self.create_tweet(self.linghu, 'hello')

        RedisClient.clear()
        conn = RedisClient.get_connection()

        key = USER_TWEETS_PATTERN.format(user_id=self.linghu.id)

        self.assertEqual(conn.exists(key), False)

        tweet2 = self.create_tweet(self.linghu, 'hello again')

        key = USER_TWEETS_PATTERN.format(user_id=self.linghu.id)
        self.assertEqual(conn.exists(key), True)

        tweets = TweetService.get_cached_tweets(self.linghu.id)
        self.assertEqual([t.id for t in tweets], [tweet2.id, tweet1.id])













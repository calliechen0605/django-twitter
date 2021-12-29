from django.test import TestCase as DjangoTestCase
from django.contrib.auth.models import User
from tweets.models import Tweet
from rest_framework.test import APIClient
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from likes.models import Like


class TestCase(DjangoTestCase):

    @property
    def anonymous_client(self):
        #instance level 的cache
        #如果同一个self进来， 不会生成新的client
        if hasattr(self, '_anonymous_client'):
            return self._anonymous_client
        self._anonymous_client = APIClient()
        return self._anonymous_client

    def create_user(self, username, email = None, password = None):
        if password is None:
            password = 'generic password'
        if email is None:
            email = f'{username}@twitter.com'
        #password will be encrypted
        return User.objects.create_user(username, email, password)

    def create_tweet(self, user, content= None):
        if content is None:
            content = 'default tweet content'
        return Tweet.objects.create(user=user, content = content)

    def create_comment(self, user, tweet, content = None):
        if content is None:
            content = 'default comment content'
        return Comment.objects.create(user = user, tweet = tweet, content = content)

    def create_like(self, user, target):
        #target is tweet or comment
        #_这个位置 -> whether to create or get, No need to know
        instance, _ =  Like.objects.get_or_create(
            content_type = ContentType.objects.get_for_model(target.__class__),
            object_id = target.id,
            user = user,
        )
        return instance


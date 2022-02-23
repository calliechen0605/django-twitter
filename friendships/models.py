from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_delete
from friendships.listeners import friendship_changed
from utils.memcached_helper import MemcachedHelper

'''
Note: 
user.tweet_set 等价于Tweet.objects.filter(user= user)

'''
class Friendship(models.Model):
    from_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null = True,
        #反查逻辑
        #set 重命名
        related_name='following_friendship_set',
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null = True,
        related_name='follower_friendship_set',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        index_together = (
            ('from_user_id', 'created_at'),
            ('to_user_id', 'created_at'),
        )
        #数据库层面去重
        unique_together = (('from_user_id', 'to_user_id'),)

    def __str__(self):
        return '{} followed {}'.format(self.from_user_id, self.to_user_id)

    @property
    def cached_from_user(self):
        return MemcachedHelper.get_object_through_cache(User, self.from_user_id)

    @property
    def cached_to_user(self):
        return MemcachedHelper.get_object_through_cache(User, self.to_user_id)


#this is for friendship changes
pre_delete.connect(friendship_changed, sender=Friendship)
post_save.connect(friendship_changed, sender=Friendship)
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import pre_delete, post_save
from likes.models import Like
from tweets.constants import TweetPhotoStatus, TWEET_PHOTO_STATUS_CHOICES
from utils.listeners import invalidate_object_cache
from utils.memcached_helper import MemcachedHelper
from utils.time_helpers import utc_now


class Tweet(models.Model):
    #如果是foreign key， 一定要用set_null. 这篇tweets谁发的
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null = True,
        help_text='who posted this tweet',
        verbose_name='Owner of this tweet'
    )#coding style, 超过了80字符， 换行。 一个parameter一行
    content = models.CharField(max_length=255)
    # 时间自动计算
    created_at = models.DateTimeField(auto_now_add=True)
    #每次修改都会更新时间
    #updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        index_together = (('user', 'created_at'),)
        #-created_at, negative sign, ascending 
        ordering = ('user', '-created_at')

    @property
    def hours_to_now(self):
        #datetime.now不带时区信息， utc有
        #datetime.now() - self.created_at)
        return (utc_now() - self.created_at).seconds // 3600

    @property
    def like_set(self):
        return Like.objects.filter(
            content_type = ContentType.objects.get_for_model(Tweet),
            object_id = self.id,
        ).order_by('-created_at')

    #java里的to_string
    def __str__(self):
        #执行 print(tweet instance会显示的内容
        return f'{self.created_at}{self.user}:{self.content}'

    @property
    def cached_user(self):
        return MemcachedHelper.get_object_through_cache(User, self.user_id)


class TweetPhoto(models.Model):

    tweet = models.ForeignKey(Tweet, on_delete=models.SET_NULL, null = True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    file = models.FileField()
    order = models.IntegerField(default=0)

    #status ==> whole number
    status = models.IntegerField(
        default = TweetPhotoStatus.PENDING,
        choices = TWEET_PHOTO_STATUS_CHOICES,
    )

    has_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        index_together = (
            ('user', 'created_at'),
            ('has_deleted', 'created_at'),
            ('status', 'created_at'),
            ('tweet', 'order'),
        )

    def __str__(self):
        return f'{self.tweet_id} : {self.file}'

pre_delete.connect(invalidate_object_cache, sender=Tweet)
post_save.connect(invalidate_object_cache, sender=Tweet)

# Create your models here.

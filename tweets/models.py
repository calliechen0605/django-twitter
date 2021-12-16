from django.db import models
from django.contrib.auth.models import  User
from  utils.time_helpers import utc_now


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

    #java里的to_string
    def __str__(self):
        #执行 print(tweet instance会显示的内容
        return f'{self.created_at}{self.user}:{self.content}'


# Create your models here.

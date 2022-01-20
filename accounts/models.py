from accounts.listeners import user_changed, user_profile_changed
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_delete

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null = True)
    avatar = models.FileField(null=True)
    nickname = models.CharField(null = True, max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {}'.format(self.user, self.nickname)


def get_profile(user):
    if hasattr(user, '_cached_user_profile'):
        return getattr(user, '_cached_user_profile')
    profile, _ = UserProfile.objects.get_or_create(user=user)
    # 使用 user 对象的属性进行缓存(cache)，避免多次调用同一个 user 的 profile 时
    # 重复的对数据库进行查询
    setattr(user, '_cached_user_profile', profile)
    return profile


# 给 User Model 增加了一个 profile 的 property 方法用于快捷访问
User.profile = property(get_profile)

pre_delete.connect(user_changed, sender=User)
post_save.connect(user_changed, sender=User)

pre_delete.connect(user_profile_changed, sender=UserProfile)
post_save.connect(user_profile_changed, sender=UserProfile)
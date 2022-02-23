from accounts.models import UserProfile
from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import caches
from twitter.cache import USER_PATTERN, USER_PROFILE_PATTERN

cache = caches['testing'] if settings.TESTING else caches['default']


class UserService(object):

    @classmethod
    def get_user_profile_through_cache(cls, user_id):
        key = USER_PROFILE_PATTERN.format(user_id)
        user_profile = cache.get(key)
        if user_profile is not None:
            return user_profile
        #not in cache then search in DB; cache miss, read from db
        user_profile, _ = UserProfile.objects.get_or_create(user_id=user_id)
        cache.set(key, user_profile)
        return user_profile

    @classmethod
    def invalidate_user_profile(cls, user_id):
        key = USER_PROFILE_PATTERN.format(user_id=user_id)
        cache.delete(key)



from friendships.models import Friendship
from django.core.cache import cache
from twitter.cache import FOLLOWINGS_PATTERN


class FriendshipService(object):

    @classmethod
    def get_followers(cls, user):

        #  alternatively
        #  friendships = Friendship.objects.filter(to_user = user)
        #  follower_ids = [friendship.from_user_id for friendship in friendships]
        # followers = User.objects.filter(id__in = follower_ids)

        friendships = Friendship.objects.filter(
            to_user = user,
        ).prefetch_related('from_user')
        return [friendship.from_user for friendship in friendships]

    @classmethod
    def has_followed(cls, current_user, obj):
        return  Friendship.objects.filter(
                from_user = current_user,
                to_user = obj,
        ).exists()

    @classmethod
    def get_following_user_id_set(cls, from_user_id):
        key = FOLLOWINGS_PATTERN.format(user_id = from_user_id)
        user_id_set = cache.get(key)
        if user_id_set is not None:
            return user_id_set

        friendships = Friendship.objects.filter(from_user_id = from_user_id)
        user_id_set = set([
            friendship.to_user_id
            for friendship in friendships
        ])
        cache.set(key, user_id_set)
        return user_id_set

    @classmethod
    def invalidate_following_cache(cls, from_user_id):
        key = FOLLOWINGS_PATTERN.format(user_id=from_user_id)
        cache.delete(key)



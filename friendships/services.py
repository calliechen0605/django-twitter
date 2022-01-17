from friendships.models import Friendship


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

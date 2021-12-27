from friendships.models import Friendship


class FriendshipService(object):

    @classmethod
    def get_followers(cls, user):

        #  alternatively
        #  friendships = Friendship.objects.filter(to_user = user)
        #  follower_ids = [friendship.from_user_id for friendship in friendships]
        # followers = User.objects.filter(id__in = follower_ids)
        #
        #select_related --> left join
        #正确写法1
        # friendship = Friendship.objects.filter(to_user = user)
        # follower_ids = [friendship.from_user_id for friendship in friendships]
        #上一句不会产生额外query，因为from_user_id已经在friendship里
        #followers = User.objects.filter(id_in = follower_ids)
        #上一句虽然不快， 但是还是比N query 快

        friendships = Friendship.objects.filter(
            to_user = user,
        ).prefetch_related('from_user')
        return [friendship.from_user for friendship in friendships]
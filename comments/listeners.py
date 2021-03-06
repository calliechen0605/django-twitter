from utils.listeners import invalidate_object_cache


def incr_comments_count(sender, instance, created, **kwargs):
    from tweets.models import Tweet
    from django.db.models import F

    if not created:
        Tweet.objects.filter(id=instance.tweet_id)\
            .update(comments_count=F('comments_count') + 1)


def decr_comments_count(sender, instance, created, **kwargs):
    from tweets.models import Tweet
    from django.db.models import F

    if not created:
        Tweet.objects.filter(id=instance.tweet_id) \
            .update(comments_count=F('comments_count') - 1)
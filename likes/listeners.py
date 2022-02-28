from utils.listeners import invalidate_object_cache


def decr_likes_count(sender, instance, **kwargs):
    from tweets.models import Tweet
    from django.db.models import F

    model_class = instance.content_type.model_class()
    if model_class != Tweet:
        return

    # cancel like
    Tweet.objects.filter(id=instance.object_id)\
        .update(likes_count=F('likes_count') - 1)
    # invalidate_object_cache(sender=Tweet, instance= instance.tweet)
    # don't update cache


def incr_likes_count(sender, instance, created, **kwargs):
    from tweets.models import Tweet
    from django.db.models import F

    if not created:
        return

    model_class = instance.content_type.model_class()
    if model_class != Tweet:
        return

    # this is an atomic operations
    # my sql has row lock
    # equiv to below SQL Query
    # UPDATE likes_count = likes_count + 1 FROM tweets_table WHERE id <= instance.object_id>
    # F function need to check docs
    # Method 1
    Tweet.objects.filter(id=instance.object_id)\
        .update(likes_count=F('likes_count') + 1)
    # invalidate_object_cache(sender=Tweet, instance=instance.tweet)
    # Method 2
    # tweet = instance.content_object
    # tweet.likes_count += 1
    # tweet.save()

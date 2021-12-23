from rest_framework import serializers
from newsfeeds.models import NewsFeed
from tweets.api.serializers import TweetSerializer
from accounts.api.serializers import UserSerializerForNewsFeed


class NewsFeedSerializer(serializers.ModelSerializer):
    tweet = TweetSerializer()
    #tweet serializer 里有user

    class Meta:
        model = NewsFeed
        fields = ('id', 'created_at', 'tweet')
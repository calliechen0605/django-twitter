from rest_framework import serializers
from newsfeeds.models import NewsFeed
from tweets.api.serializers import TweetSerializer
<<<<<<< Updated upstream
from accounts.api.serializers import UserSerializerForNewsFeed
=======
>>>>>>> Stashed changes


class NewsFeedSerializer(serializers.ModelSerializer):
    tweet = TweetSerializer()
<<<<<<< Updated upstream
    #tweet serializer 里有user
=======
>>>>>>> Stashed changes

    class Meta:
        model = NewsFeed
        fields = ('id', 'created_at', 'tweet')
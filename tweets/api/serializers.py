from rest_framework import serializers
from tweets.models import  Tweet
from accounts.api.serializers import UserSerializer, UserSerializerForTweet
from comments.api.serializers import CommentSerializer

#model serializer 默认实现好fields
#不同的serializer --> 不同接口对同一个object解析要求不一样
class TweetSerializer(serializers.ModelSerializer):
    user = UserSerializerForTweet() #每个field还可以是另外的serializer, 如果这里不specify user serializer, 就会return userID 而不是完整的user 信息

    class Meta:
        model = Tweet
        fields = ('id', 'user', 'created_at', 'content')


class TweetSerializerWithComments(serializers.ModelSerializer):
    #queryset
    comments = CommentSerializer(source = 'comment_set', many=True) #每个field还可以是另外的serializer, 如果这里不specify user serializer, 就会return userID 而不是完整的user 信息

    class Meta:
        model = Tweet
        fields = ('id', 'user', 'created_at', 'content', 'comments')

#modelSerillizer的话， 需要指定是哪个model
class TweetSerializerForCreate(serializers.ModelSerializer):
    content = serializers.CharField(min_length=6, max_length=140)

    class Meta:
        model = Tweet
        fields = ('content',)

    #.save的时候
    def create(self, validated_data):
        user = self.context['request'].user
        content = validated_data['content']
        tweet = Tweet.objects.create(user=user, content = content)
        return tweet

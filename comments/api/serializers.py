from accounts.api.serializers import UserSerializerForComment
from comments.models import Comment
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from tweets.models import Tweet

#view一般尽量用generic，避免用model， 但是serializer用model好的
class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializerForComment()

    class Meta:
        model = Comment
        fields = ('id',
                  'tweet_id',
                  'user',
                  'content',
                  'created_at',
                  'updated_at',
                  )

class CommentSerializerForCreate(serializers.ModelSerializer):
    #默认的model serializer 只有user和tweet，其实我有看到tweet_id啦。。
    tweet_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

    class Meta:
        model = Comment
        fields = ('content', 'tweet_id', 'user_id')

    def validated(self, data):
        tweet_id = data['tweet_id']
        if not Tweet.objects.filter(id = tweet_id).exists():
            raise ValidationError({'message' : 'tweet does not exist'})
        return data

    def create(self, validated_data):
        return Comment.objects.create(
            user_id = validated_data['user_id'],
            tweet_id = validated_data['tweet_id'],
            content  = validated_data['content'],
        )


#update is different from create, because users are not allow to update tweet_id or user_id
class CommentSerializerForUpdate(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('content', )

        def update(self, instance, validated_data):
            instance.content = validated_data['content']
            instance.save()
            #update requires to return updated instance
            return instance
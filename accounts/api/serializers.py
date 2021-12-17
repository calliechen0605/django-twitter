from django.contrib.auth.models import User
from rest_framework import serializers, exceptions


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class UserSerializerForTweet(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username')


class UserSerializerForFriendship(UserSerializerForTweet):
    pass


#serializer - 两个作用
#渲染用户object to json
#valiadation input info
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        if not User.objects.filter(username=data['username'].lower()).exists():
            raise exceptions.ValidationError({
                'username': 'user doesnt exist.'
            })
        return data

#seriaizer. save()可以创建用户
class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=20, min_length=6)
    password = serializers.CharField(max_length=20, min_length=6)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
    #will be called when is_valid is called
    def validate(self, data):
        #忽视大小写的match -- 但是这个效率低
        #User.objects.filter(username__iexact = data['username']).exist()
        #所以存的时候就要小写
        if User.objects.filter(username=data['username'].lower()).exists():
            raise exceptions.ValidationError({
                'username': 'This username has been occupied.'
            })
        if User.objects.filter(email=data['email'].lower()).exists():
            raise exceptions.ValidationError({
                'email': 'This email address has been occupied.'
            })
        return data

    def create(self, validated_data):
        #存储的时候都是小写
        username = validated_data['username'].lower()
        email = validated_data['email'].lower()
        password = validated_data['password']

        # encrypted password, email and password normalize
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        return user


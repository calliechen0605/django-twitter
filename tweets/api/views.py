from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from tweets.api.serializers import TweetSerializer, TweetSerializerForCreate
from tweets.models import Tweet

#model view set 尽量不要用，model view set支持增删查改， 但很多时候 接口需要有限制
'''
class TweetViewSet(viewsets.GenericViewSet, 
                   viewsets.mixins.CreateModelMixin,
                   viewsets.mixins.ListModelMixin):
'''
class TweetViewSet(viewsets.GenericViewSet):
    #API endpoint that allows users to create and list tweets
    #queryset = Tweet.objects.all()
    serializer_class = TweetSerializerForCreate

    #多个函数
    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()] #更直白， list 谁都可以访问
        return [IsAuthenticated()]

    #def list(self, request, *args, **kwargs):
    def list(self, request):
        if 'user_id' not in request.query_params: #check是不是带了userID
            return Response('missing user_id', status=400)
        user_id=request.query_params['user_id'] # return in char， 但是会自动做转换
        tweets = Tweet.objects.filter(user_id=user_id).order_by('-created_at')   #取出所有tweets
        serializer = TweetSerializer(tweets, many = True) #when many = true, will return list of dicts
        return Response({'tweets':serializer.data}) #response 约定return dict

    def create(self, request):
        serializer = TweetSerializerForCreate(
            data = request.data,
            context = {'request' : request},
        )
        if not serializer.is_valid():
            return Response({
                "success" : False,
                "message": "Please check input.",
                "error": serializer.errors,
            }, status=400)
        #save will triger create method in TweetSerializierForCreate
        tweet = serializer.save()
        #
        return Response(TweetSerializer(tweet).data, status=201)



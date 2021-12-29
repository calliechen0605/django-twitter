from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from tweets.api.serializers import TweetSerializer, TweetSerializerForCreate, TweetSerializerWithComments
from tweets.models import Tweet
from newsfeeds.services import NewsFeedService
from utils.decorators import required_params


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
    queryset = Tweet.objects.all()

    #多个函数
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()] #更直白， list 谁都可以访问
        return [IsAuthenticated()]

    def retrieve(self, request, *args, **kwargs):
        # <HOMEWORK 1> 通过某个 query 参数 with_all_comments 来决定是否需要带上所有 comments
        # <HOMEWORK 2> 通过某个 query 参数 with_preview_comments 来决定是否需要带上前三条 comments
        #没有指定queryset, get_object不知道从哪里拿
        tweet = self.get_object()
        return Response(TweetSerializerWithComments(tweet).data)

    #def list(self, request, *args, **kwargs):
    @required_params(params=['user_id'])
    def list(self, request, *args, **kwargs):
        '''
        if 'user_id' not in request.query_params: #check是不是带了userID
            return Response('missing user_id', status=400)
            #this is replaced by decorator
        '''
        # return in char， 但是会自动做转换
        user_id=request.query_params['user_id']
        # 取出所有tweets
        tweets = Tweet.objects.filter(user_id=user_id).order_by('-created_at')
        # when many = true, will return list of dicts
        serializer = TweetSerializer(tweets, many = True)
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
        #view简单的事情， 复杂逻辑换去别的地方
        NewsFeedService.fanout_to_followers(tweet)
        return Response(TweetSerializer(tweet).data, status=201)



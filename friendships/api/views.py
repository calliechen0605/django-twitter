
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from friendships.api.paginations import FriendshipPagination
from friendships.models import Friendship
from friendships.api.serializers import (
    FollowingSerializer,
    FollowerSerializer,
    FriendshipSerializerForCreate,
)
from django.contrib.auth.models import User


class FriendshipViewSet(viewsets.GenericViewSet):
    serializer_class = FriendshipSerializerForCreate
    queryset = User.objects.all()
    pagination_class = FriendshipPagination

    @action(methods=['GET'], detail=True, permission_classes = [AllowAny])
    def followers(self, request, pk):
        #GET / api/friendships/1/followers/
        friendships = Friendship.objects.filter(to_user_id=pk).order_by('-created_at')
        page = self.paginate_queryset(friendships)
        serializer = FollowerSerializer(
            page,
            many = True,
            context={'request' : request},
        )
        return self.get_paginated_response(serializer.data)

    @action(methods=['GET'], detail=True, permission_classes = [AllowAny])
    def followings(self, request, pk):
        #GET / api/friendships/1/followers/
        friendships = Friendship.objects.filter(from_user_id=pk).order_by('-created_at')
        page = self.paginate_queryset(friendships)
        serializer = FollowingSerializer(
            page,
            many=True,
            context={'request': request},
        )
        return self.get_paginated_response(serializer.data)

    @action(methods=['POST'], detail=True, permission_classes = [IsAuthenticated])
    def follow(self, request, pk):
        #post会默认要一个serializer
        #website就是登录的人要follow 的id
        # /api/friendships/<pk>/follow/
        #get if user with id = pk exists
        #self.get_object()
        serializer = FriendshipSerializerForCreate(data = {
            'from_user_id' : request.user.id,
            'to_user_id' : pk,
        })
        #can add an decorator for serializer_error_check
        if not serializer.is_valid():
            return Response({
                'success' : False,
                'errors' : serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
        instance = serializer.save()
        return Response(
            FollowingSerializer(instance, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
        )


    @action(methods=['POST'], detail=True, permission_classes = [IsAuthenticated])
    def unfollow(self, request, pk):
        unfollow_user = self.get_object()
        #pk是string
        if request.user.id == unfollow_user.id:
            return Response({
                'success' : False,
                'message' : 'You cannot unfollow yourself',
            }, status=status.HTTP_400_BAD_REQUEST)

        #deleted --> 一共删除
        #_ --> hashtable with all the info
        #cascade --> database 可能会翻车
        #on_delete = models.SET_NULL
        deleted, _ = Friendship.objects.filter(
            from_user=request.user,
            to_user=unfollow_user,
        ).delete()
        return Response({'success' : True, 'deleted' : deleted})

    #MySQL
    #不用join, cascade, drop foreign key constraint


    def list(self, request):
        return Response({'message' : 'this is friendship home page'})
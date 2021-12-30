from likes.api.serializers import (
    LikeSerializer,
    LikeSerializerForCreate,
    LikeSerializerForCancel,
)
from likes.models import Like
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from utils.decorators import required_params


class LikeViewSet(viewsets.GenericViewSet):
    queryset = Like.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializerForCreate

    @required_params(request_attr='data', params=['content_type', 'object_id'])
    def create(self, request, *args, **kwargs):
        serializer = LikeSerializerForCreate(
            data = request.data,
            context = {'request' : request},
        )
        if not serializer.is_valid():
            return Response({
                'message': 'Please check input',
                'errors':serializer.errors,
            }, status = status.HTTP_400_BAD_REQUEST)
        instance = serializer.save()
        return Response(
            LikeSerializer(instance).data,
            status=status.HTTP_201_CREATED,
        )

    #不需要对应ID
    @action(methods=['POST'], detail= False)
    @required_params(request_attr='data', params=['content_type', 'object_id'])
    def cancel(self, request):
        serializer = LikeSerializerForCancel(
            data = request.data,
            context = {'request': request},
        )
        if not serializer.is_valid():
            return Response({
                'message' : 'Please check input',
                'errors' : serializer.errors,
            }, status = status.HTTP_400_BAD_REQUEST)
        #需要在serializer里实现
        deleted = serializer.cancel()
        return Response({
            'success':True,
            'deleted' : deleted,
        }, status = status.HTTP_200_OK)

    #没有找到就cancel的情况 -- cancel可能比like先到,不一定先到后到，
    #用缓存解决
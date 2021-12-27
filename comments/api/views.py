from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from comments.models import Comment
from comments.api.serializers import (
    CommentSerializer,
    CommentSerializerForCreate,
)

#尽量用generic views
class CommentViewSet(viewsets.GenericViewSet):
    """
    只实现list, create, update, destroy
    """
    serializer_class = CommentSerializerForCreate  # 在django 界面渲染
    queryset = Comment.objects.all()

    # 默认6个方法
    # POST /api/comments/  ->  create
    # GET /api/comments/   ->   list
    # GET /api/comments/1/   ->   retrieve
    # DELETE /api/comments/1/   ->   destroy
    # PATCH /api/comments/1/   ->   partial_update
    # PUT /api/comments/1/   ->   update

    #检测action 判断permission
    def get_permissions(self):
        if self.action == 'create':
            # 要用 IsAuthenticated() instantiate,
            return [IsAuthenticated()]
        return [AllowAny()]
    #self.get_object()就会找上面的queryset

    def create(self, request, *args, **kwargs):
        data = {
            'user_id'  : request.user.id,
            'tweet_id' : request.data.get('tweet_id'),
            'content' : request.data.get('content'),
        }
        serializer = CommentSerializerForCreate(data = data)
        if not serializer.is_valid():
            return Response({
                'message' : 'Please check input',
                'error' : serializer.errors,
            }, status = status.HTTP_400_BAD_REQUEST)

        comment = serializer.save()
        return Response(
            CommentSerializer(comment).data,
            status=status.HTTP_201_CREATED,
        )
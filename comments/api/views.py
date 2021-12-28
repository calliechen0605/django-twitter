from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from comments.models import Comment
from comments.api.serializers import (
    CommentSerializer,
    CommentSerializerForCreate,
    CommentSerializerForUpdate,
)
from comments.api.permissions import IsObjectOwner

#尽量用generic views
class CommentViewSet(viewsets.GenericViewSet):
    """
    只实现list, create, update, destroy
    """
    serializer_class = CommentSerializerForCreate  # 在django 界面渲染
    queryset = Comment.objects.all()
    filterset_fields = ('tweet_id', )

    # 默认6个方法
    # POST /api/comments/  ->  create
    # GET /api/comments/   ->   list
    # GET /api/comments/1/   ->   retrieve
    # DELETE /api/comments/1/   ->   destroy
    # PATCH /api/comments/1/   ->   partial_update
    # PUT /api/comments/1/   ->   update

    #检测action 判断permission
    #这个好fancy啊
    def get_permissions(self):
        if self.action == 'create':
            # 要用 IsAuthenticated() instantiate,
            return [IsAuthenticated()]
        if self.action in ['update', 'destroy']:
            return [IsAuthenticated(), IsObjectOwner()] #按顺序检测
        return [AllowAny()]
    #self.get_object()就会找上面的queryset

    def list(self, request, *args, **kwargs):
        if 'tweet_id' not in request.query_params:
            return Response(
                {
                    'message' : 'missing tweet_id in the request',
                    'success' : False,
                },
                status = status.HTTP_400_BAD_REQUEST,
            )
        #get 到默认的query set
        queryset = self.get_queryset()
        comments = self.filter_queryset(queryset).order_by('created_at')
        serializer = CommentSerializer(comments, many = True)
        return Response(
            {
                'comments' : serializer.data,
            }, status = status.HTTP_200_OK,
        )

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

    #update一定要传instance
    def update(self, request, *args, **kwargs):
        #get_object 是 DRF的包装函数， 找不到会raise 404
        # no need to do extra check
        comment = self.get_object()
        serializer = CommentSerializerForUpdate(
            instance = comment,
            data = request.data,
        )
        if not serializer.is_valid():
            raise Response({
                'message' : 'Please check input',
            }, status = status.HTTP_400_BAD_REQUEST)
        #save 会触发serializer里的update
        #save 根据 instance 有没有被传进来决定是 create 还是 update
        comment = serializer.save()
        return Response(
            CommentSerializer(comment).data,
            status = status.HTTP_200_OK,
        )

    #delete
    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        comment.delete()
        #DRF default return is 204 no content
        # here we returned 200
        return Response({'success': True}, status = status.HTTP_200_OK)


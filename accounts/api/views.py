from accounts.api.serializers import (
    LoginSerializer,
    SignupSerializer,
    UserProfileSerializerForUpdate,
    UserSerializer,
    UserSerializerWithProfile,
)
from accounts.models import UserProfile
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import (
    authenticate as django_authenticate,
    login as django_login,
    logout as django_logout,
)
from accounts.api.serializers import SignupSerializer, LoginSerializer
from utils.permissions import IsObjectOwner


class UserViewSet(viewsets.ModelViewSet):
    """
    modelviewset --> default的配置有llist, retrieve, put, patch, destroy
    """
    queryset = User.objects.all()
    serializer_class = UserSerializerWithProfile
    permission_classes = (permissions.IsAdminUser,)


class AccountViewSet(viewsets.ViewSet):
    serializer_class = UserSerializer
    #主资源下的次目录叫action, /api/accounts/login_status --> 这里login_status 就是action
    #detail: url不需要写ID， 不是某个object, (整体目录false,specific  id  true)
    @action(methods=['GET'], detail=False)
    def login_status(self, request):
        data = {'has_logged_in': request.user.is_authenticated}
        if request.user.is_authenticated:
            #data 加入user信息, return login status + user info
            #formatting 成json
            data['user'] = UserSerializer(request.user).data
        return Response(data)

    #指定get, post会return 405
    @action(methods=['POST'], detail=False)
    def logout(self, request):
        django_logout(request)
        return Response({"success": True})

    @action(methods=['POST'], detail=False)
    def login(self, request):
        #get  username and password from request
        #如果是get, request.get_params
        serializer = LoginSerializer(data=request.data)
        #validate input format
        #status code default 200
        # is_valid 之后， 就可以调errors, property
        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Please check input",
                "errors": serializer.errors,
            }, status=400)

        #validation ok ,login
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        #if user doesnt exist
        #queryset.query打印结果可以看

        # user for login (after authentication)
        user = django_authenticate(username=username, password=password)
        if not user or user.is_anonymous:
            return Response({
                "success": False,
                "message": "username and password does not match",
            }, status=400)
        django_login(request, user)
        return Response({
            "success": True,
            "user": UserSerializerWithProfile(user).data,
        })

    @action(methods=['POST'], detail=False)
    def signup(self, request):
        #没有传具体的instance是创建
        #SignupSerializer(instance = user, data=request.data) -- 这个是更新
        serializer = SignupSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': "Please check input",
                'errors': serializer.errors,
            }, status=400)
        #create new instance
        user = serializer.save()
        django_login(request, user)

        return Response({
            'success': True,
            'user': UserSerializerWithProfile(user).data,
        }, status = 201)


class UserProfileViewSet(
    viewsets.GenericViewSet,
    viewsets.mixins.UpdateModelMixin,
):
    queryset = UserProfile
    permission_classes = (permissions.IsAuthenticated, IsObjectOwner)
    serializer_class = UserProfileSerializerForUpdate



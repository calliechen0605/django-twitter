from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from accounts.api.serializers import (
    UserSerializer,
    LoginSerializer,
    SignupSerializer,
)
from django.contrib.auth import (
    logout as django_logout,
    login as django_login,
    authenticate as django_authenticate,
)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #每个操作检测 --》需要 登录
    permission_classes = [permissions.IsAuthenticated]



class AccountViewSet(viewsets.ViewSet):
    serializer_class = SignupSerializer
    @action(methods=['GET'], detail = False)
    def login_status(self, request):
        data = {'has_logged_in': request.user.is_authenticated}
        if request.user.is_authenticated:
            data['user'] = LoginSerializer (request.user).data
        return  Response(data)

    @action(methods=['POST'], detail = False)
    def logout(self, request):
        django_logout(request)
        return Response({'success' : True})

    @action(methods=['POST'], detail = False)
    def login(self, request):
        #get username, password from request
        serializer = LoginSerializer(data = request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({
                "success" :  False,
                "message" : "Please check input",
                "errors" : serializer.errors, #is valid -> errors (property)
            }, status = 400)#bad request, client error

        #data after validation, if ok login
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        #in case user doesn't exist
        if not User.objects.filter(username = username).exists():
            return Response({
                "success" : False,
                "message" : "User doesnt exist.",
            }, status = 400)
        #only the  authenticated can be qualified as user
        user = django_authenticate(username = username, password = password)
        if not user or user.is_anonymous:
            return Response({
                "success" : False,
                "message" : "username and password doesnt match",
            }, status = 400)

        django_login(request, user)
        return Response({
            "success" : True,
            "user" : UserSerializer(user).data,
        })

    @action(methods=['POST'], detail = False)
    def signup(self, request):
        serializer = SignupSerializer(data = request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({
                "success" : False,
                "message" : "Please check input.",
                "errors": serializer.errors,
            }, status = 400)

        user = serializer.save()
        django_login(request, user)
        return Response({
            'success' : True,
            'user' : UserSerializer(user).data,
        }, status = 201)

















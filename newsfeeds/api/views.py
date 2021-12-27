from rest_framework import viewsets, status
from rest_framework.decorators import permission_classes
<<<<<<< Updated upstream
from rest_framework.permissions import IsAuthenticated
=======
from rest_framework.permissions import  IsAuthenticated
>>>>>>> Stashed changes
from rest_framework.response import Response
from newsfeeds.models import NewsFeed
from newsfeeds.api.serializers import NewsFeedSerializer

<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
class NewsFeedViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return NewsFeed.objects.filter(user = self.request.user)

    def list(self, request):
        serializer = NewsFeedSerializer(self.get_queryset(), many = True)
        return Response({
<<<<<<< Updated upstream
            'newsfeeds': serializer.data,
        }, status = status.HTTP_200_OK)
=======
            'newsfeeds' : serializer.data,
        }, status = status.HTTP_200_OK)
>>>>>>> Stashed changes

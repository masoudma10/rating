from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Avg, Count, F, Sum
from ..models import Post, Rating
from .serializer import PostSerializer, RatingSerializer
from django.core.cache import cache
from datetime import datetime, timedelta
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from django.utils.timezone import now
from django.db import transaction


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Rating.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        user = request.user
        post_id = request.data.get('post')
        score = request.data.get('score')

        rating, created = Rating.objects.update_or_create(
            user=user,
            post_id=post_id,
            defaults={'score': score}
        )
        serializer = self.get_serializer(rating)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

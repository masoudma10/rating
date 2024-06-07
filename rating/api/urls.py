# posts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import PostViewSet, RatingViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'rate', RatingViewSet, basename='rating')

urlpatterns = [
    path('', include(router.urls)),
]
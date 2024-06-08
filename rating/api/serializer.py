from rest_framework import serializers
from ..models import Post, Rating


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['score']


# class PostSerializer(serializers.ModelSerializer):
#     ratings_count = serializers.IntegerField(source='ratings.count', read_only=True)
#     ratings_average = serializers.SerializerMethodField()
#     user_rating = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Post
#         fields = ['id', 'title', 'content', 'ratings_count', 'ratings_average', 'user_rating']
#
#     def get_ratings_average(self, obj):
#         return obj.weighted_average_rating
#
#     def get_user_rating(self, obj):
#         request = self.context.get('request')
#         if request and request.user.is_authenticated:
#             rating = Rating.objects.filter(post=obj, user=request.user).first()
#             return rating.score if rating else None
#         return None


class PostSerializer(serializers.ModelSerializer):
    ratings_count = serializers.IntegerField(source='ratings.count', read_only=True)
    ratings_average = serializers.FloatField(source='normalized_average_rating', read_only=True)
    user_rating = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'ratings_count', 'ratings_average', 'user_rating']

    def get_user_rating(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            rating = Rating.objects.filter(post=obj, user=request.user).first()
            return rating.score if rating else None
        return None
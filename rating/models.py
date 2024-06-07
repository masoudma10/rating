from utils.base_model import BaseModel
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg, StdDev
from django.utils import timezone

class Post(BaseModel):
    title = models.CharField(max_length=255)
    content = models.TextField()

    @property
    def weighted_average_rating(self):
        total_weighted_score = 0
        total_weights = 0
        now = timezone.now()

        for rating in self.ratings.all():
            time_diff = (now - rating.created_at).total_seconds() / 3600
            weight = max(1, 24 - time_diff)
            total_weighted_score += rating.score * weight
            total_weights += weight

        return total_weighted_score / total_weights if total_weights > 0 else None

    def __str__(self):
        return self.title

    @property
    def normalized_average_rating(self):
        ratings = self.ratings.all()
        if not ratings.exists():
            return None

        avg_rating = ratings.aggregate(avg=Avg('score'))['avg']
        stddev_rating = ratings.aggregate(stddev=StdDev('score'))['stddev']

        if stddev_rating is None or stddev_rating == 0:
            return avg_rating

        normalized_scores = [
            (rating.score - avg_rating) / stddev_rating
            for rating in ratings
        ]

        normalized_avg_rating = sum(normalized_scores) / len(normalized_scores)
        return normalized_avg_rating

    def __str__(self):
        return self.title


class Rating(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    weighted_score = models.FloatField(default=0.0)

    class Meta:
        unique_together = ('post', 'user')
        indexes = [
            models.Index(fields=['post', 'user']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.post.title}: {self.score}"

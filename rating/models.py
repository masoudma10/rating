from utils.base_model import BaseModel
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg, StdDev
from django.utils import timezone
from django.db.models import F, Sum, FloatField, ExpressionWrapper, DurationField
from django.db.models.functions import Coalesce, Extract


class Post(BaseModel):
    title = models.CharField(max_length=255)
    content = models.TextField()

    @property
    def weighted_average_rating(self):
        now = timezone.now()
        ratings = self.ratings.annotate(
            time_diff_hours=ExpressionWrapper(
                Extract(now - F('created_at'), 'epoch') / 3600.0,
                output_field=FloatField()
            )
        ).annotate(
            weight=Coalesce(24.0 - F('time_diff_hours'), 1.0)
        ).aggregate(
            total_weighted_score=Sum(F('score') * F('weight'), output_field=FloatField()),
            total_weights=Sum('weight', output_field=FloatField())
        )

        total_weighted_score = ratings['total_weighted_score']
        total_weights = ratings['total_weights']

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


class Rating(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    class Meta:
        unique_together = ('post', 'user')
        indexes = [
            models.Index(fields=['post', 'user']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.post.title}: {self.score}"

from django.db import models

# Create your models here.
# posts/models.py
from django.contrib.auth.models import User

# Post model to handle image uploads and captions
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/')
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}\'s post'

# Like model to track post likes
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} liked {self.post}'

# Comment model for post comments
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} commented on {self.post}'

class Fixture(models.Model):
    home_team = models.CharField(max_length=255)
    away_team = models.CharField(max_length=255)
    sport = models.CharField(max_length=100)
    round_number = models.IntegerField(default=1)
    points_home = models.IntegerField(default=0)
    points_away = models.IntegerField(default=0)
    man_of_the_match = models.CharField(max_length=255, blank=True, null=True)  # New field

    def _str_(self):
        return f"{self.sport}: {self.home_team} vs {self.away_team} (Round {self.round_number})"
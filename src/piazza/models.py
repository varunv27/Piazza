from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Post(models.Model):
    TECH = 'tech'
    SPORT = 'sport'
    HEALTH = 'health'
    POLITICS = 'politics'

    TOPIC_CHOICES = (
        (TECH, 'Tech'),
        (SPORT, 'Sport'),
        (HEALTH, 'Health'),
        (POLITICS, 'Politics'),
    )
    ACTIVE = 'active'
    EXPIRED = 'expired'

    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (EXPIRED, 'Expired'),
    )

    title = models.CharField(max_length=300)
    topic = models.CharField(max_length=300, choices=TOPIC_CHOICES)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expiry_date = models.DateTimeField()
    status = models.CharField(max_length=300, choices=STATUS_CHOICES, default='active')
    owner = models.ForeignKey(User, related_name='blog_posts', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    # def get_total_likes(self):
    #     return self.likes.users.count()
    #
    # def get_total_dis_likes(self):
    #     return self.dis_likes.users.count()

    @property
    def has_expired(self):
        return timezone.now() > self.expiry_date

    def expiry_duration(self):
        e = self.expiry_date - timezone.now()
        if e.total_seconds() < 0:
            return 0
        return e.total_seconds()

    def set_status(self):
        if self.has_expired:
            return self.EXPIRED

        return self.status


class Like(models.Model):
    post = models.OneToOneField(Post, related_name='likes', on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='post_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.post.title


class Dislike(models.Model):
    post = models.OneToOneField(Post, related_name='dis_likes', on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='post_dis_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.post.title


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return str(self.message)[:30]

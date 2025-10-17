from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class FriendRequest(models.Model):
    """Friend request system"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('cancelled', 'Cancelled'),
    ]
    
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_requests_sent')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_requests_received')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(blank=True, help_text="Optional message with the friend request")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('from_user', 'to_user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username} ({self.status})"

    @property
    def is_pending(self):
        return self.status == 'pending'

    @property
    def is_accepted(self):
        return self.status == 'accepted'

    @property
    def is_declined(self):
        return self.status == 'declined'

class Friendship(models.Model):
    """Friendship relationship between users"""
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships_initiated')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships_received')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user1.username} <-> {self.user2.username}"

    @classmethod
    def are_friends(cls, user1, user2):
        """Check if two users are friends"""
        return cls.objects.filter(
            models.Q(user1=user1, user2=user2) | 
            models.Q(user1=user2, user2=user1)
        ).exists()

    @classmethod
    def get_friends(cls, user):
        """Get all friends of a user"""
        friendships = cls.objects.filter(
            models.Q(user1=user) | models.Q(user2=user)
        )
        friends = []
        for friendship in friendships:
            if friendship.user1 == user:
                friends.append(friendship.user2)
            else:
                friends.append(friendship.user1)
        return friends

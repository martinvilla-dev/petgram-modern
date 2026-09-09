from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    website = models.URLField(max_length=200, blank=True)
    bio = models.TextField()
    display_name = models.CharField(max_length=40)
    profile_pic = models.ImageField(upload_to='profile_img', null=True, blank=True)
    follows = models.ManyToManyField('self', related_name='user_follows', symmetrical=False, blank=True, default='self')
    CHOICES = (
        ('Dog', 'Dog'),
        ('Cat', 'Cat'),
        ('Hamster', 'Hamster'),
        ('Bird', 'Bird'),
        ('Fish', 'Fish'),
        ('Reptile', 'Reptile'),
        ('Others', 'Others'),
    )
    pet_type = models.CharField(max_length=300, choices = CHOICES)
    followers = models.ManyToManyField('self', related_name='user_followers', symmetrical=False, blank=True, default='self')

    # Added to resolve the reverse accessor clash with auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='customuser_set',
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customuser_set',
        related_query_name='customuser',
    )

    def __str__(self):
        return self.display_name
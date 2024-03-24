from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
import os
from django.contrib.auth import get_user_model
from django.db.models import Q

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

STATUS = ((0, "Closed"), (1, "Open"))
ROLES = ((0, "User"), (1, "Service Provider"))

def image_file_path(instance, filename):
    return f'images/{instance.username}.jpg'



class ChatManager(models.Manager):
    def by_user(self, **kwargs):
        user = kwargs.get('user')
        lookup = models.Q(user1=user) | models.Q(user2=user)
        result = self.get_queryset().filter(lookup).distinct()
        return result

class ChatWindow(models.Model):
    user1 = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='user1_chats')
    user2 = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='user2_chats')
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ChatManager()

    class Meta:
        unique_together = ['user1', 'user2']

    def clean(self):
        if self.user1 == self.user2:
            raise ValidationError("User1 and User2 can't be same.")
        elif ChatWindow.objects.filter(user1=self.user2, user2=self.user1).exists():
            raise ValidationError("Conversation between the users already exists")

    def _str_(self):
        return f"Conversation between {self.user1} and {self.user2}"


class ChatMessage(models.Model):
    chat_window = models.ForeignKey(ChatWindow, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def _str_(self):
        return f"Message from {self.user} in conversation between {self.chat_window.user1} and {self.chat_window.user2}"

class Profile(User):
    role = models.IntegerField(choices=ROLES, default=0)
    photo = models.ImageField(upload_to=image_file_path, null=True)

    def _str_(self):
        return self.first_name + " " + self.last_name

    def save(self, *args, **kwargs):
        try:
            old_profile = Profile.objects.get(pk=self.pk)
            if old_profile.photo and self.photo and old_profile.photo != self.photo:
                # Delete old profile picture file from storage
                os.remove(old_profile.photo.path)
        except Profile.DoesNotExist:
            pass

        super(Profile, self).save(*args, **kwargs)


# class Post(models.Model):
#     id = models.AutoField(primary_key=True)
#     title = models.CharField(max_length=30)
#     content = models.TextField()
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_on = models.DateTimeField(auto_now_add=True)
#     status = models.IntegerField(choices=STATUS, default=0)
#
#     def __str__(self):
#         return self.title


class Cargaragedata(models.Model):
    name = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=3,decimal_places=1)
    address = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=20)
    website = models.URLField()

    def __str__(self):
        return self.name


class ChatManager(models.Manager):
    def by_user(self, **kwargs):
        user = kwargs.get('user')
        lookup = models.Q(user1=user) | models.Q(user2=user)
        result = self.get_queryset().filter(lookup).distinct()
        return result

# feedback/models.py

class Feedback(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user}"

class CarService(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='car_service_images/', null=True, blank=True)

    def __str__(self):
        return self.title

class ServiceForm(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()
    GARAGE_CHOICES = [
        ('garage1', 'Garage 1'),
        ('garage2', 'Garage 2')
    ]
    garage = models.CharField(max_length=20, choices=GARAGE_CHOICES)

    def __str__(self):
        return self.firstname + ' ' + self.lastname


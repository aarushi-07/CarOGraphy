from django.contrib.auth.models import User
from django.db import models
import os

STATUS = ((0, "Closed"), (1, "Open"))
ROLES = ((0, "User"), (1, "Service Provider"))


def image_file_path(instance, filename):
    return f'images/{instance.username}.jpg'


class Profile(User):
    role = models.IntegerField(choices=ROLES, default=0)
    photo = models.ImageField(upload_to=image_file_path, null=True)

    def __str__(self):
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

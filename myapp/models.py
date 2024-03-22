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

<<<<<<< HEAD
# Arish
# extending django built in User class
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(upload_to=image_file_path, blank=True, null=True)
    role = models.CharField(max_length=20, choices=(('client', 'Client'), ('service_provider', 'Service Provider')))
    # created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} Profile'

# whenever a new user is added @receiver decorator listens for a post save for a new user and creates the user profile part 
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.profile.save()
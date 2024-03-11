from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

STATUS = ((0, "Closed"), (1, "Open"))
ROLES = ((0, "User"), (1, "Service Provider"))


def image_file_path(instance, filename):
    return 'images/{instance.email}.jpg'


# Create your models here.
class CarUser(models.Model):
    # id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=50, primary_key=True)
    password = models.CharField(max_length=20)
    role = models.IntegerField(choices=ROLES, default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to=image_file_path, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


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

# Arish
# extending django built in User class
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(upload_to=image_file_path, blank=True, null=True)
    role = models.CharField(max_length=20, choices=(('client', 'Client'), ('service_provider', 'Service Provider')))
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} Profile'

# whenever a new user is added @receiver decorator listens for a post save for a new user and creates the user profile part 
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.profile.save()
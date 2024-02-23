from django.db import models

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

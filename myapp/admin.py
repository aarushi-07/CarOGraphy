from django.contrib import admin
from .models import CarUser#, Post
from .models import *
# Register your models here.
admin.site.register(CarUser)
#admin.site.register(Post)
admin.site.register(UserProfile)
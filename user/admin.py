from django.contrib import admin
from django.contrib.auth.models import User

from user.models import CustomUser

admin.site.register(CustomUser)
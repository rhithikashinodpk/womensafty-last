from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import *
# Register your models here.
admin.site.register(User,UserAdmin),
admin.site.register(PoliceProfile),
admin.site.register(UserProfile)
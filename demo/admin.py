from django.contrib import admin
from demo.models import (
    Profile,
    ProfileLogs
)
# Register your models here.
admin.site.register(Profile)
admin.site.register(ProfileLogs)
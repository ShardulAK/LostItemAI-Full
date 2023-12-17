from django.contrib import admin
from .models import Found_img, Profile
# Register your models here.
# Register model to admin pannel so that we can view it there
admin.site.register(Found_img)
admin.site.register(Profile)

from django.contrib import admin
from .models import User,OneTimePassword,Profile

admin.site.register(User)
admin.site.register(OneTimePassword)
admin.site.register(Profile)
# Register your models here.

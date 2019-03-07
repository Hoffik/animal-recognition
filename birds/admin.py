from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Recording, Bird, Evaluation

admin.site.register(User, UserAdmin)
admin.site.register(Recording)
admin.site.register(Bird)
admin.site.register(Evaluation)
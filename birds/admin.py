from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Project, Right, Tag, Record, Weight, Identification

admin.site.register(User, UserAdmin)
admin.site.register(Project)
admin.site.register(Right)
admin.site.register(Tag)
admin.site.register(Record)
admin.site.register(Weight)
admin.site.register(Identification)
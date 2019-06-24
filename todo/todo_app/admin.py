from django.contrib import admin

from .models import Todo_Post, Todo_Group, Todo_Msg, Todo_Comment

admin.site.register(Todo_Post)
admin.site.register(Todo_Group)
admin.site.register(Todo_Msg)
admin.site.register(Todo_Comment)

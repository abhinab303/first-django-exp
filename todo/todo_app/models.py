from django.db import models
from django.contrib.auth.models import User, Permission
from django import forms

class Todo_Group(models.Model):
    group_name = models.CharField(max_length = 100)
    #group_admin = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
    group_users = models.ManyToManyField(User)
    group_slug = models.SlugField(max_length = 40)
    GROUP_TYPE_CHOICES = (
        ('CLOSED', 'Closed'),
        ('OPEN', 'Open'),
        ('FREE', 'Free'),
    )
    group_type = models.CharField(
        max_length = 10,
        choices = GROUP_TYPE_CHOICES,
        default = 'OPEN',
    )

    def __str__(self):
        return self.group_name

class Todo_Post(models.Model):
    post_text = models.TextField(max_length = 100)
    add_date = models.DateTimeField('date added', null = True)
    owner = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
    post_group = models.ForeignKey(Todo_Group, on_delete = models.CASCADE, null = True)
    post_slug = models.SlugField(max_length = 40)
    image = models.ImageField(
        upload_to = 'todo_app/img/',
        max_length = 1000,
        null = True,
    )

    def __str__(self):
        return self.post_text

def delete_post_permission(sender, instance, **kwargs):
    Permission.objects.filter(codename__endswith = 'post_' + str(instance.id)).delete()

models.signals.post_delete.connect(
    receiver = delete_post_permission,
    sender = Todo_Post,
)

def delete_group_permission(sender, instance, **kwargs):
    Permission.objects.filter(codename__exact = 'group_su_' + str(instance.id)).delete()

models.signals.post_delete.connect(
    receiver = delete_group_permission,
    sender = Todo_Group,
)

class Todo_Msg(models.Model):
    msg_text = models.TextField(max_length = 100)
    msg_to_user = models.ManyToManyField(User)
    msg_from_user_id = models.CharField(max_length = 100, null = True)
    msg_group = models.ForeignKey(Todo_Group, on_delete = models.CASCADE, null = True)

class Todo_Comment(models.Model):
    text = models.TextField(max_length = 200)
    post = models.ForeignKey(Todo_Post, on_delete = models.CASCADE, null = True)
    vote = models.IntegerField(null = True)
    date = models.DateTimeField(null = True)
    owner = models.ForeignKey(User, on_delete = models.CASCADE, null = True)

def delete_cmnt_permission(sender, instance, **kwargs):
    Permission.objects.filter(codename__endswith = 'cmnt_' + str(instance.id)).delete()

models.signals.post_delete.connect(
    receiver = delete_cmnt_permission,
    sender = Todo_Comment,
)

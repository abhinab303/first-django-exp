# Generated by Django 2.1.7 on 2019-05-15 12:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Todo_Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=100)),
                ('group_slug', models.SlugField(max_length=40)),
                ('group_type', models.CharField(choices=[('CLOSED', 'Closed'), ('OPEN', 'Open'), ('FREE', 'Free')], default='OPEN', max_length=10)),
                ('group_users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Todo_Msg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg_text', models.TextField(max_length=100)),
                ('msg_from_user_id', models.CharField(max_length=100)),
                ('msg_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todo_app.Todo_Group')),
                ('msg_to_user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Todo_Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_text', models.TextField(max_length=100)),
                ('add_date', models.DateTimeField(null=True, verbose_name='date added')),
                ('post_slug', models.SlugField(max_length=40)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post_group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='todo_app.Todo_Group')),
            ],
        ),
    ]
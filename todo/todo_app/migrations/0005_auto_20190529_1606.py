# Generated by Django 2.1.7 on 2019-05-29 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0004_todo_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo_comment',
            name='vote',
            field=models.IntegerField(null=True),
        ),
    ]
# Generated by Django 2.1.7 on 2019-05-15 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo_msg',
            name='msg_from_user_id',
            field=models.CharField(max_length=100, null=True),
        ),
    ]

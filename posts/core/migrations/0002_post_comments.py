# Generated by Django 4.2.1 on 2023-05-23 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='comments',
            field=models.TextField(default='[]'),
        ),
    ]

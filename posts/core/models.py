from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=10000)

class Comment(models.Model):
    post_id = models.IntegerField()
    text = models.TextField(max_length=1000)

    class Meta:
        app_label = 'comments'  # Set the app_label to match the comments service app
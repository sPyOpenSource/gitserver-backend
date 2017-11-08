from django.db import models


class Item(models.Model):
    creationdate = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    description = models.TextField()


class Message(models.Model):
    creationdate = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(Item)
    text = models.TextField()

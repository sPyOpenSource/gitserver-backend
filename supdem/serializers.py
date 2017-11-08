from rest_framework import serializers
from .models import Item, Message


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'creationdate', 'title', 'description')


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'creationdate', 'item', 'text')

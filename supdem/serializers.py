from rest_framework import serializers
from .models import MyUser, Item, Message, Wiki


class MyUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MyUser
        fields = ('url', 'username')


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'creationdate', 'title', 'description', 'owner')


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'creationdate', 'item', 'owner', 'text')


class WikiSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Wiki
        fields = ('id', 'title')

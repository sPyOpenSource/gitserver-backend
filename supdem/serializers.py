from rest_framework import serializers
from .models import MyUser, Category, CategoryQuestion, Item


class MyUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MyUser
        fields = ('url', 'email')

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'poster', 'is_offer', 'active_dialogue', 'creationdate', 'expirydate', 'category', 'title', 'description', 'image')

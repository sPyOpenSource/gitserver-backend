from rest_framework import serializers
from .models import MyUser, Category, CategoryQuestion, Item


class MyUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MyUser
        fields = ('url', 'email')

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name_en')

class CategoryQuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CategoryQuestion
        fields = ('id', 'name_en')

class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'poster', 'centre', 'is_offer', 'active_dialogue', 'creationdate')

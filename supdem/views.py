from django.shortcuts import redirect
from .models import Item, Message
from supdem.serializers import ItemSerializer, MessageSerializer
from rest_framework import viewsets
from django_filters import rest_framework as filters


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class MessageViewSet(viewsets.ModelViewSet):
    """
    List all messages, or create a new message.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('item',)


def index(request):
    return redirect('/git/index.html')

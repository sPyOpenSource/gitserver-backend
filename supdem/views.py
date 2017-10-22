from datetime import datetime, timedelta

from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.middleware import csrf

from .helpers import send_template_email, reset
from .models import Item, Message, ResetPasswordKey, MyUser
from .forms import AddUserForm, NewPasswordForm, ResetPasswordForm, ItemFilter
from supdem.serializers import MyUserSerializer, ItemSerializer, MessageSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import viewsets, filters
from rest_framework import status
from rest_framework.permissions import AllowAny


class DefaultsMixin(object):
    """Default settings for view authentication, permissions, filtering
     and pagination."""
    filter_backends = [filters.DjangoFilterBackend]


class ItemViewSet(DefaultsMixin, viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_class = ItemFilter


class MessageList(APIView):
    """
    List all messages, or create a new message.
    """
    def get(self, request, format=None):
        item = request.GET.get('item')
        if item:
            item = Item.objects.get(id=item)
            queryset = Message.objects.filter(item=item)
        else:
            queryset = Message.objects.all()
        serializer_class = MessageSerializer(queryset, many=True, context={'request': request})
        return Response(serializer_class.data)

    def post(self, request, format=None):
        serializer_class = MessageSerializer(data=request.data, context={'request': request})
        if serializer_class.is_valid():
            serializer_class.save()
            message = Message.objects.get(id=serializer_class.data['id'])
            if message.item.owner.id != message.owner.id:
                send_template_email(
                    message.item.owner,
                    'message_received',
                    {
                        'message': message.text,
                        'title': message.item.title
                    },
                    message.owner
                )
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)


class MyUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer


def csrf_token(request):
    return JsonResponse({'csrf_token': csrf.get_token(request)})


def additem(request):
    if request.method == 'POST':
        user = MyUser.objects.get(id=request.POST['owner'])
        expirydate = request.POST.get('expirydate')
        if expirydate:
            expirydate = datetime.strptime(expirydate, '%Y-%m-%dT%H:%M:%S')
        else:
            expirydate = datetime.now() + timedelta(days=settings.ITEM_LIFETIME_IN_DAYS)
        item = Item(
            owner=user,
            expirydate=expirydate,
            title=request.POST['title'],
            description=request.POST['description']
        )
        item.save()
        return redirect('/static/index.html')


def index(request):
    return redirect('/static/index.html')


def resetpassword(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            qs = MyUser.objects.filter(email=form.cleaned_data['email'])
            if qs.count() == 1:
                user = qs[0]
                reset(user)
                return redirect('/static/index.html')
        else:
            validkeys = ResetPasswordKey.objects.filter(
                expirydate__gt=datetime.utcnow(),
                key=request.POST['key']
            )
            if validkeys.count() == 1:                 # there should be exactly one row with a valid key
                form = NewPasswordForm(request.POST)
                if form.is_valid():
                    user = validkeys[0].user               # set the new password
                    user.set_password(form.cleaned_data['password'])
                    user.save()
                    validkeys.delete()                      # this key is not needed anymore
                    auth_user = authenticate(               # authenticate the user in with his new password
                        email=user.email,
                        password=form.cleaned_data['password']
                    )
                    login(request, auth_user)               # log the user in
                    messages.success(request, _('The password has been changed'))
                    return HttpResponseRedirect(reverse('index'))


def adduser(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST, request=request)
        if form.is_valid():
            messages.success(request, _('User was successfully added'))
            user = form.cleaned_data['user']
            reset(user)
            return JsonResponse({'status': 201})

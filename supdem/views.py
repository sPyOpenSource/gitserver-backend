from datetime import datetime, timedelta
from cloudinary import uploader
import re

from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.signing import TimestampSigner
from django.core.urlresolvers import reverse
from django.db.models import Count, F, Q
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponseNotAllowed, \
    Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import get_language
from django.utils.translation import ugettext as _
from django.utils.crypto import get_random_string
from django.contrib.auth.models import Group
from django.middleware import csrf

from .helpers import send_template_email
from .models import Category, Centre, Item, \
    Message, ResetPasswordKey, MyUser
from .forms import AddUserForm, AddDialogueForm, AddMessageForm, LoginForm, NewPasswordForm, \
    ResetPasswordForm, ItemFilter
from supdem.serializers import MyUserSerializer, ItemSerializer, CategorySerializer, GroupSerializer, MessageSerializer

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


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ItemViewSet(DefaultsMixin, viewsets.ModelViewSet):
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


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    permission_classes = (AllowAny,)
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


def image(request):
    if request.method == 'POST':
        image_name = ""
        if 'photo' in request.FILES:
            cloudinary_photo = uploader.upload(request.FILES['photo'])
            if 'public_id' in cloudinary_photo:
                image_name = cloudinary_photo['public_id']
        user = MyUser.objects.get(id=request.POST['owner'])
        category = Category.objects.get(id=request.POST['category'])
        expirydate = request.POST.get('expirydate')
        if expirydate:
            expirydate = datetime.strptime(expirydate, '%Y-%m-%dT%H:%M:%S')
        else:
            expirydate = datetime.now() + timedelta(days=settings.ITEM_LIFETIME_IN_DAYS)
        item = Item(
            owner=user,
            expirydate=expirydate,
            category=category,
            title=request.POST['title'],
            description=request.POST['description'],
            image=image_name
        )
        item.save()
        return redirect('/static/index.html')
    return JsonResponse({'csrf_token': csrf.get_token(request)})


def index(request):
    return redirect('/static/index.html')


def demo(request):
    expirydate = request.GET.get('expirydate')
    if expirydate:
        list_params = {'expirydate__gt': datetime.strptime(expirydate, '%Y-%m-%dT%H:%M:%S')}
    else:
        list_params = {'expirydate__gt': datetime.utcnow()}
    items = []
    for item in Item.objects.filter(**list_params).order_by('-creationdate'):
        items.append({'title': item.title, 'image': item.image, 'owner': item.owner.username, 'category': item.category.name, 'id': item.id, 'creationdate': item.creationdate})
    return JsonResponse(items, safe = False)


def resetpassword(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            qs = MyUser.objects.filter(email=form.cleaned_data['email'])
            if qs.count() == 1:
                user = qs[0]
                # delete old keys if they exist
                ResetPasswordKey.objects.filter(user=user).delete()
                newresetpasswordkey = ResetPasswordKey(
                    user=user,
                    key=get_random_string(20),
                    expirydate=datetime.utcnow() + timedelta(hours=settings.PASSWORD_RESET_PERIOD_IN_HOURS)
                )
                newresetpasswordkey.save()
                messages.success(request, _('An email with a password recovery link has been send to you'))
                send_template_email(user, 'password_reset', {
                    'url': '/static/index.html#password/' + newresetpasswordkey.key
                })
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
            send_template_email(user, 'account_created')
            return redirect('/static/index.html#/success')

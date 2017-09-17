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
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


def image(request):
    if request.method == 'POST':
        if 'photo' in request.FILES:
            cloudinary_photo = uploader.upload(request.FILES['photo'])
            if 'public_id' in cloudinary_photo:
                image_name = cloudinary_photo['public_id']
            else:
                image_name = ""
        else:
            image_name = ""
        user = MyUser.objects.get(id=request.POST.get('owner',''))
        category = Category.objects.get(id=request.POST.get('category',''))
        item = Item(
            owner=user,
            expirydate=datetime.now() + timedelta(days=settings.ITEM_LIFETIME_IN_DAYS),
            category=category,
            title=request.POST.get('title',''),
            description=request.POST.get('description',''),
            image=image_name
        )
        item.save()
        return redirect('/static/index.html')
    context = {
        'categories': Category.objects.all(),
        'owner': request.GET.get('owner','')
    }
    return JsonResponse({'csrf_token': csrf.get_token(request)})


def index(request):
    list_params = {'expirydate__gt': datetime.utcnow()}
    context = {
        'items': Item.objects.filter(**list_params).order_by('-creationdate')
    }
    return render(request, 'supdem/index.html', context)


def newpassword(request):
    context = {}
    validkeys = ResetPasswordKey.objects.filter(
        expirydate__gt=datetime.utcnow(),
        key=request.GET.get('key')
    )
    if validkeys.count() != 1:                 # there should be exactly one row with a valid key
        form_success = False
        messages.error(request, _('Invalid code. Please request a new code.'))
        form = None                            # we don't need a form if the key is invalid
        print 'here'
    elif request.method == 'POST':             # we have a form submission
        form = NewPasswordForm(request.POST)
        form_success = form.is_valid()
    else:
        form_success = False                   # this was the first request for theis page
        form = NewPasswordForm()
    if form_success:
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
    context['form'] = form
    return render(request, 'supdem/newpassword.html', context)


def resetpassword(request):
    context = {}
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        form_success = form.is_valid()
    else:
        form_success = False
        form = ResetPasswordForm()
    if form_success:
        qs = MyUser.objects.filter(email=form.cleaned_data['email'])
        if qs.count() != 1:
            form_success = False
            context['unknown_email'] = 1
    if form_success:
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
            'url': reverse('newpassword') + "?key=" + newresetpasswordkey.key
        })
        return redirect('/')
    context['form'] = form
    return render(request, 'supdem/resetpassword.html', context)


def adduser(request):
    groups = Group.objects.all()
    if request.method == 'POST':
        form = AddUserForm(request.POST, request=request)
        if form.is_valid():
            messages.success(request, _('User was successfully added'))
            user = form.cleaned_data['user']
            send_template_email(user, 'account_created')
            return redirect('/static/index.html')
    return render(request, 'supdem/adduser.html', {'groups': groups})

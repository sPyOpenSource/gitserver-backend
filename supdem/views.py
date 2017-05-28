from datetime import datetime, timedelta
from cloudinary import uploader
import re

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.signing import TimestampSigner
from django.core.urlresolvers import reverse
from django.db.models import Count, F, Q
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponseNotAllowed, \
    Http404
from django.shortcuts import render, get_object_or_404
from django.utils.translation import get_language
from django.utils.translation import ugettext as _
from django.utils.crypto import get_random_string

from.helpers import send_template_email
from .models import Category, CategoryQuestionOption, Centre, Dialogue, Item, \
    Message, Photo, QuestionOption, ResetPasswordKey, MyUser, CategoryQuestion
from .forms import AddItemForm, AddDialogueForm, AddMessageForm, LoginForm, NewPasswordForm, \
    ResetPasswordForm
from rest_framework import viewsets
from supdem.serializers import MyUserSerializer, ItemSerializer, CategorySerializer, CategoryQuestionSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryQuestionViewSet(viewsets.ModelViewSet):
    queryset = CategoryQuestion.objects.all()
    serializer_class = CategorySerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class MyUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer

def index(request, centreslug=None, usertype=None):
    redirect_needed = 0
    if centreslug:
        # we don't want to store the slug in the session if it is invalid
        centre = get_object_or_404(Centre, slug=centreslug)
        request.session['centreslug'] = centreslug
    elif not request.GET.get('ignoreses') and 'centreslug' in request.session:
        centreslug = request.session['centreslug']
        redirect_needed = 1
    if usertype:
        request.session['usertype'] = usertype
    elif not request.GET.get('ignoreses') and 'usertype' in request.session:
        usertype = request.session['usertype']
        redirect_needed = 1
    if redirect_needed:
        if centreslug and usertype:
            return HttpResponseRedirect(reverse(
                'list', kwargs={'centreslug': centreslug, 'usertype': usertype}))
        if centreslug and not usertype:
            return HttpResponseRedirect(reverse('index', kwargs={'centreslug': centreslug}))
        if not centreslug and usertype:
            return HttpResponseRedirect(reverse('index', kwargs={'usertype': usertype}))

    centre = get_object_or_404(Centre, slug=centreslug) if centreslug else None
    context = {
        'centres': Centre.centres_with_numitems(),
        'usertype': usertype,
        'centre': centre,
        'is_index': 1,
    }
    return render(request, 'supdem/index.html', context)


def list_view(request, centreslug, usertype):
    centre = get_object_or_404(Centre, slug=centreslug)
    request.session['centreslug'] = centreslug
    request.session['usertype'] = usertype

    # Create the category filter data
    cur_cat_filter = request.GET.get('cf')
    if cur_cat_filter:
        cur_cat_filter = int(cur_cat_filter)
    filter_params = {}
    list_params = {
        'expirydate__gt': datetime.utcnow(),
        'centre': centre,
        'active_dialogue': 0,
        'is_offer': (usertype == 'refugee')
    }
    filter_params = dict(('item__' + key, value) for (key, value) in list_params.items())
    base_url = reverse('list', kwargs={'centreslug': centreslug, 'usertype': usertype})
    categories = Category.objects.filter(**filter_params).annotate(
        num_items=Count('item', distinct=True)
    )
    filter_categories = []
    for cat in categories:
        filter_categories.append({
            'is_current_filter': cur_cat_filter and cat.id == cur_cat_filter,
            'id': cat.id,
            'filter_url': base_url + "?cf=" + str(cat.id),
            'num_items': cat.num_items
        })

    # create option filter data
    # todo jas: add real num_items
    filter_options = []
    current_option_filters = {}
    if cur_cat_filter:
        category = get_object_or_404(Category, pk=cur_cat_filter)
        regexp = re.compile(r"^of\d+$")
        current_option_filters = \
            dict((key[2:], 1) for (key, value) in request.GET.items() if regexp.search(key))

        # add where clauses to the final item query
        list_params['category'] = category
        for opt_id in current_option_filters.keys():
            list_params['questionoption__answer'] = \
                get_object_or_404(CategoryQuestionOption, pk=opt_id)

        # count the nr of items for the next option filters
        filter_params = dict(('questionoption__item__' + key, value)
                             for (key, value) in list_params.items())
        cqo = CategoryQuestionOption.objects.filter(**filter_params).annotate(
            num_items=Count('questionoption', distinct=True)
        )
        items_per_opt = dict((opt.id, opt.num_items) for opt in cqo)

        # get the options so we can show them in a list (per question)
        options = CategoryQuestionOption.objects.filter(
            categoryquestion__category=category
        ).order_by('categoryquestion', 'order')
        questions_with_selection = dict((opt.categoryquestion.id, opt.id)
                                        for opt in options
                                        if str(opt.id) in current_option_filters)

        # go over all options and build a structure for the template
        question_index = -1
        prev_question_id = 0
        clear_option_filter_url = ''
        for opt in options:
            question_id = opt.categoryquestion.id
            if prev_question_id != question_id:
                question_index += 1
                prev_question_id = question_id
                clear_option_filter_url = base_url + "?cf=" + str(category.id) + \
                    ''.join(';of' + str(opt_id) + '=1' for (que_id, opt_id) in
                            questions_with_selection.items() if que_id != question_id)
                filter_options.append({
                    'id': question_id,
                    'clear_option_filter_url': clear_option_filter_url,
                    'has_selection': question_id in questions_with_selection,
                    'options': []
                })
            filter_options[question_index]['options'].append({
                'is_current_filter': str(opt.id) in current_option_filters,
                'id': opt.id,
                'filter_url': clear_option_filter_url + ';of' + str(opt.id) + '=1',
                'num_items': items_per_opt[opt.id] if opt.id in items_per_opt else 0
            })

    # create result list (this is what it is all about....)
    items_list = Item.objects.filter(**list_params).order_by('-creationdate')
    paginator = Paginator(items_list, settings.MAX_ITEMS_IN_LIST)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    context = {
        'usertype': usertype,
        'centre': centre,
        'items': items,
        'is_itemlist': 1,
        'filter_categories': filter_categories,
        'filter_options': filter_options,
        'categories': Category.objects.all()
    }
    return render(request, 'supdem/list.html', context)


def item(request, centreslug, usertype, itemid):
    item = get_object_or_404(Item, pk=itemid)
    user = request.user
    user_is_poster = user.is_authenticated() and user == item.poster
    context = {
        'usertype': usertype,
        'centre': get_object_or_404(Centre, slug=centreslug),
        'item': item,
        'user_is_poster': user_is_poster,
        'can_manage': user_is_poster,
        'is_expired': item.expirydate.replace(tzinfo=None) < datetime.utcnow(),
    }
    if item.centre != context['centre'] or item.for_usertype() != usertype:
        raise Http404("Item not found")

    # if there is an active dialogue, show the add message form
    active_dialogue = get_object_or_404(Dialogue, pk=item.active_dialogue)\
        if user.is_authenticated() and item.active_dialogue else 0
    if active_dialogue and (user_is_poster or user == active_dialogue.reactor):
        if request.method == 'POST':
            form = AddMessageForm(request.POST)
            form_success = form.is_valid()
        else:
            form = AddMessageForm()
            form_success = False
        if form_success:
            newmessage = Message(
                dialogue=active_dialogue,
                from_poster=user_is_poster,
                description=form.cleaned_data['description'],
                languagecode=get_language()
            )
            newmessage.save()
            active_dialogue.last_change = newmessage.creationdate
            active_dialogue.save()
            messages.success(request, _('Your reaction was successfully added'))
            receiver = active_dialogue.reactor if user_is_poster else item.poster
            send_template_email(receiver, 'message_received', {
                'url': item.url(),
                'title': item.title
            })
            # because we are returning to the same page, we will need a new empty form
            form = AddMessageForm()
        context['can_manage'] = 1
        context['form'] = form

    # if the user is logged in, see if we can find and relevant dialogues
    dialogues = Dialogue.objects.filter(
        Q(item=item), Q(reactor=user) | Q(item__poster=user)
    ).order_by('-last_change') if user.is_authenticated() else []
    # if there are dialogues, collect them with the info we need for showing them
    # process the form first, for in case somebody just added a message
    for dialogue in dialogues:
        # performance note: it is more efficient to retrieve all notes for all dialogues
        # together, but this is easier to read and in most cases, there are only one or two
        # dialogues per item
        notes = dialogue.message_set.all().order_by('creationdate')
        for row in notes:
            row.is_by_this_user = bool(row.from_poster) == user_is_poster
        dialogue.notes = notes
        receiver = dialogue.reactor if user_is_poster else item.poster
        dialogue.the_other_username = receiver.username
        dialogue.is_active = dialogue.id == item.active_dialogue
    context['dialogues'] = dialogues
    return render(request, 'supdem/item.html', context)


def deleteitem(request, centreslug, usertype, itemid):
    centre = get_object_or_404(Centre, slug=centreslug)
    items = Item.objects.filter(
        id=itemid,
        expirydate__gt=datetime.utcnow(),
        centre=centre,
        is_offer=usertype == 'refugee'
    )
    if items.count() != 1:
        return HttpResponseForbidden()
    item = items[0]
    user = request.user
    if user.is_authenticated() and user == item.poster:
        item.expirydate = datetime.utcnow()
        item.save()
    else:
        return HttpResponseForbidden()
    # if there is a dialogue, end it and inform the reactor
    if item.active_dialogue:
        dialogue = get_object_or_404(Dialogue, pk=item.active_dialogue)
        dialogue.end_dialogue()
        send_template_email(dialogue.reactor, 'item_deleted', {
            'url': item.url(),
            'title': item.title,
            'ender_username': user.username
        })
    messages.success(request, _('The item was successfully deleted'))
    return HttpResponseRedirect(reverse('mypage'))


def extenditem(request, centreslug, usertype, itemid):
    centre = get_object_or_404(Centre, slug=centreslug)
    items = Item.objects.filter(
        id=itemid,
        expirydate__gt=datetime.utcnow(),
        centre=centre,
        is_offer=usertype == 'refugee'
    )
    if items.count() != 1:
        return HttpResponseForbidden()
    item = items[0]
    if not request.user.is_authenticated() or request.user != item.poster:
        return HttpResponseForbidden()
    item.expirydate = datetime.utcnow() + timedelta(days=settings.ITEM_LIFETIME_IN_DAYS)
    item.save()
    messages.success(request, _('The item was successfully extended'))
    return HttpResponseRedirect(item.url())


# todo jas: check the centreslug and usertype
def deletedialogue(request, centreslug, usertype, dialogueid):
    dialogue = get_object_or_404(Dialogue, pk=dialogueid)
    item = dialogue.item
    user = request.user
    if not user.is_authenticated() or item.active_dialogue != dialogue.id:
        return HttpResponseForbidden()
    if user == item.poster or user == dialogue.reactor:
        dialogue.end_dialogue()
    else:
        return HttpResponseForbidden()
    the_other_user = dialogue.reactor if bool(user == item.poster) else item.poster
    send_template_email(the_other_user, 'dialogue_ended', {
        'url': item.url(),
        'title': item.title,
        'ender_username': user.username
    })
    messages.success(request, _('The claim was successfully deleted'))
    return HttpResponseRedirect(reverse('mypage'))


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
    if request.user.is_authenticated():
        return HttpResponseForbidden()
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
        # disable the old password
        user.password = 'x'
        user.save()
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
    context['form'] = form
    return render(request, 'supdem/resetpassword.html', context)


def login_view(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    form = LoginForm(request.POST)
    if form.is_valid():
        user = authenticate(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )
        if user:
            login(request, user)
        else:
            messages.error(request, _('Incorrect username and/or password'))
    else:
        messages.error(request, _('Incorrect username and/or password'))
    return HttpResponseRedirect(request.POST.get('url'))


# we can not redirect to the list page because we don't know the usertype and centre. But that is
# not a problem as a logout means that a new user will be using the website.
# I am not redirecting to the page the user came from, as this might be a page that is only
# for authenticated users.
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")


# this page shows a list with items that this person added and reactions from this person
def mypage(request):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseForbidden()
    dialogues = Dialogue.objects.filter(
        reactor=user,
        item__expirydate__gt=datetime.utcnow(),
        item__active_dialogue__exact=F('id')
    ).order_by('-last_change')
    items_list = Item.objects.filter(
        poster=user,
        expirydate__gt=datetime.utcnow(),
    ).order_by('-creationdate')
    paginator = Paginator(items_list, settings.MAX_ITEMS_IN_LIST)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    context = {
        'items': items,
        'dialogues': dialogues,
        'is_mypage': 1,
        'user': user,
    }
    return render(request, 'supdem/mypage.html', context)


def adddialogue(request, centreslug, usertype, itemid):
    item = Item.objects.filter(
        id=itemid,
        expirydate__gt=datetime.utcnow(),
        active_dialogue=0
    )[0]
    centre = get_object_or_404(Centre, slug=centreslug)
    if request.method == 'POST':
        form = AddDialogueForm(request.POST, request=request)
        if form.is_valid():
            user = form.cleaned_data['user']
            if form.cleaned_data['is_new_user']:
                send_template_email(user, 'account_created')

            newdialogue = Dialogue(
                item=item,
                reactor=user,
                last_change=datetime.utcnow(),
            )
            newdialogue.save()
            newmessage = Message(
                dialogue=newdialogue,
                from_poster=False,
                description=form.cleaned_data['description'],
                languagecode=get_language()
            )
            newmessage.save()
            # flag the item as "claimed" or "in dialogue"
            item.active_dialogue = newdialogue.id
            item.save()
            # send an email to the item poster
            send_template_email(item.poster, 'message_received', {
                'url': item.url(),
                'title': item.title
            })
            # send a notification to the reactor
            messages.success(request, _('Your reply was send to the poster of the item'))
            # show the item detail page
            return HttpResponseRedirect(item.url())
    else:
        # these texts should not be gettext translated as we want people to write eachother
        # in English.
        if item.is_offer:
            descr = "Hi %(name)s,\n\nI'm interested in this item. Please get in touch!"
        else:
            descr = "Hi %(name)s,\n\nI can help you with this. Let's find out how to get it to you"
        form = AddDialogueForm(initial={
            'timestamp': TimestampSigner().sign(request.session.session_key),
            'description': descr % {'name': item.poster.username}
        })
    context = {
        'item': item,
        'usertype': usertype,
        'centre': centre,
        'form': form
    }
    return render(request, 'supdem/adddialogue.html', context)


def additem(request, centreslug, usertype):
    cat = get_object_or_404(Category, pk=request.GET.get('catid'))
    centre = get_object_or_404(Centre, slug=centreslug)

    # don't accept form posts if the centre is not active
    if request.method == 'POST' and centre.is_active:
        form = AddItemForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            user = form.cleaned_data['user']
            # if the user was new, send him an email
            if form.cleaned_data['is_new_user']:
                send_template_email(user, 'account_created')
            # if a photo was uploaded, store it at cloudinary
            if 'photo' in request.FILES:
                cloudinary_photo = uploader.upload(request.FILES['photo'])
                image_name = cloudinary_photo['public_id'] \
                    if 'public_id' in cloudinary_photo else ""
            else:
                image_name = ""
            newitem = Item(
                poster=user,
                centre=centre,
                is_offer=bool(usertype == 'local'),
                expirydate=datetime.utcnow() + timedelta(days=settings.ITEM_LIFETIME_IN_DAYS),
                category=cat,
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                image=image_name
            )
            newitem.save()
            for catque in cat.categoryquestion_set.all():
                newanswer = QuestionOption(
                    item=newitem,
                    answer=get_object_or_404(
                        CategoryQuestionOption,
                        pk=request.POST.get('catque-' + str(catque.id))
                    )
                )
                newanswer.save()
            # store reference to photo locally
            if image_name:
                Photo(item=newitem, image=image_name).save()
            messages.success(request, _('The item was successfully added'))
            return HttpResponseRedirect(newitem.url())
    else:
        form = AddItemForm(initial={
            'timestamp': TimestampSigner().sign(request.session.session_key)
        })
    context = {
        'category': cat,
        'usertype': usertype,
        'centre': centre,
        'extra_questions': cat.categoryquestion_set.all(),
        'form': form
    }
    return render(request, 'supdem/additem.html', context)

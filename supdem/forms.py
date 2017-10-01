import django_filters

from django import forms
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.core.signing import SignatureExpired, TimestampSigner
from django.shortcuts import get_object_or_404
from django.utils.translation import get_language
from django.utils.translation import ugettext as _

from .models import Category, Item, MyUser


class ItemFilter(django_filters.FilterSet):
    expirydate = django_filters.DateFilter(name='expirydate', lookup_expr='gt')

    class Meta:
        model = Item
        fields = ('expirydate',)


# abstract form that can be used by all other forms that accept logged in users,
# new users and users who are not logged in, but have an account.
class LoginAndModifyForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(LoginAndModifyForm, self).__init__(*args, **kwargs)

    new_username = forms.CharField(max_length=50, required=False)
    new_password = forms.CharField(max_length=50, widget=forms.PasswordInput, required=False)
    new_email = forms.EmailField(required=False)
    existing_password = forms.CharField(max_length=50, widget=forms.PasswordInput, required=False)
    existing_email = forms.EmailField(required=False)
    timestamp = forms.CharField(max_length=200, widget=forms.HiddenInput)

    # hope fully this protects against most of the spam bots. If you realy want,
    # you can get through this check.
    def clean_timestamp(self):
        timestamp = self.cleaned_data['timestamp']
        # accepts a form for an hour
        try:
            msg = TimestampSigner().unsign(timestamp, max_age=60 * 60)
        except SignatureExpired:
            raise forms.ValidationError(_("You waited too long with filling out the form"))
        if msg != self.request.session.session_key:
            raise forms.ValidationError(_("please enable cookies"))
        return timestamp

    def clean(self):
        super(LoginAndModifyForm, self).clean()

        self.cleaned_data['is_new_user'] = False
        if self.request.user.is_authenticated():
            user = self.request.user
        else:
            if self.cleaned_data['new_email']:
                email_exists = MyUser.objects.filter(email=self.cleaned_data['new_email']).count()
                if email_exists:
                    raise forms.ValidationError(_("Email address already in use"))
                if not self.cleaned_data['new_username']:
                    raise forms.ValidationError(_("Username required for creating a new user"))
                if not self.cleaned_data['new_password']:
                    raise forms.ValidationError(_("Password required for creating a new user"))
                newuser = MyUser.objects.create_user(
                    username=self.cleaned_data['new_username'],
                    email=self.cleaned_data['new_email'],
                    password=self.cleaned_data['new_password'],
                    languagecode=get_language()
                )
                newuser.save()
                self.cleaned_data['is_new_user'] = True
                new_or_existing = 'new'
            else:
                new_or_existing = 'existing'
            user = authenticate(
                email=self.cleaned_data[new_or_existing + '_email'],
                password=self.cleaned_data[new_or_existing + '_password'],
            )
            if user is None:
                raise forms.ValidationError(_("The username and password were incorrect."))
            login(self.request, user)
        self.cleaned_data['user'] = user
        return self.cleaned_data


class AddUserForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(AddUserForm, self).__init__(*args, **kwargs)

    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)
    email = forms.EmailField()
    group_id = forms.IntegerField()

    def clean(self):
        super(AddUserForm, self).clean()
        email_exists = MyUser.objects.filter(email=self.cleaned_data['email']).count()
        if email_exists:
            raise forms.ValidationError(_("Email address already in use"))
        if not self.cleaned_data['password']:
            raise forms.ValidationError(_("Password required for creating a new user"))
        newuser = MyUser.objects.create_user(
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            group_id=self.cleaned_data['group_id'],
            username=self.cleaned_data['username']
        )
        newuser.save()
        self.cleaned_data['user'] = newuser
        return self.cleaned_data


class AddDialogueForm(LoginAndModifyForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'direction': 'ltr'}))

    def clean(self):
        super(AddDialogueForm, self).clean()

        if not self.cleaned_data['user'].can_start_dialogue():
            raise forms.ValidationError(_("Maximum number of claims reached"))
        return self.cleaned_data


class AddMessageForm(forms.Form):
    description = forms.CharField(widget=forms.Textarea(attrs={'direction': 'ltr'}))


class LoginForm(forms.Form):
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)
    email = forms.EmailField()


class ResetPasswordForm(forms.Form):
    email = forms.EmailField()


class NewPasswordForm(forms.Form):
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)

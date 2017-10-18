import django_filters

from django import forms
from django.utils.translation import ugettext as _

from .models import Item, MyUser


class ItemFilter(django_filters.FilterSet):
    expirydate = django_filters.DateFilter(name='expirydate', lookup_expr='gt')

    class Meta:
        model = Item
        fields = ('expirydate',)


class AddUserForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(AddUserForm, self).__init__(*args, **kwargs)

    email = forms.EmailField()

    def clean(self):
        super(AddUserForm, self).clean()
        email_exists = MyUser.objects.filter(email=self.cleaned_data['email']).count()
        if email_exists:
            raise forms.ValidationError(_("Email address already in use"))
        newuser = MyUser.objects.create_user(
            email=self.cleaned_data['email'],
            username='new user'
        )
        newuser.save()
        self.cleaned_data['user'] = newuser
        return self.cleaned_data


class ResetPasswordForm(forms.Form):
    email = forms.EmailField()


class NewPasswordForm(forms.Form):
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# Register your models here.
from .models import Centre, Category, CategoryQuestion, CategoryQuestionOption, Item

admin.site.register(Centre)
admin.site.register(Item)
admin.site.register(Category)

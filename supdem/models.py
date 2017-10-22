from django.db import models
from django.conf import settings
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.core.urlresolvers import reverse


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            username='admin',
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Item(models.Model):
    creationdate = models.DateTimeField(auto_now_add=True)
    expirydate = models.DateTimeField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    owner = models.ForeignKey(MyUser)

    def __str__(self):
        return self.title


class Message(models.Model):
    creationdate = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(Item)
    text = models.TextField()
    owner = models.ForeignKey(MyUser)


class ResetPasswordKey(models.Model):
    user = models.OneToOneField(MyUser)
    key = models.CharField(max_length=200, unique=True)
    expirydate = models.DateTimeField()


class EmailLog(models.Model):
    creationdate = models.DateTimeField(auto_now_add=True)
    to_user = models.ForeignKey(MyUser)
    email_name = models.CharField(max_length=50)
    status = models.PositiveSmallIntegerField()


# I just created this so I have a place to write debug messages. :-D
# I will remove it before the site goes in production
class DebugLog(models.Model):
    creationdate = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

from django.db import models
from django.conf import settings
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, group_id, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            group_id=group_id
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
            password=password,
            group_id=1
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
    group = models.ForeignKey(Group)
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

################################
# Our own classes follow below #
################################
class Centre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    countrycode = models.CharField(max_length=2)
    latitude = models.FloatField()
    longitude = models.FloatField()
    is_active = models.BooleanField(default=True)
    show_message_for_refugees = models.BooleanField(default=False)
    show_message_for_locals = models.BooleanField(default=False)

    def __str__(self):
            return self.name

    @classmethod
    def centres_with_numitems(cls):
        """
        Returns all centres with the nr of items per center.

        Note that the query is quite tricky as I also need centres without items.
        Furthermore, the two SUM(IF())'s are written in this way to give the correct answer
        in cases where there are no items for a specific center, as i.is_offer would be NULL
        in that case.
        """
        if settings.USE_MYSQL:
            sql = """
        SELECT
            c.*,
            SUM(IF(i.id IS NULL,0,1)) as numitems_total,
            SUM(IF(i.is_offer = 0,1,0)) as numitems_fromrefugees,
            SUM(IF(i.is_offer = 1,1,0)) as numitems_fromlocals
        FROM supdem_centre c LEFT JOIN supdem_item i
        ON
            i.centre_id = c.id AND
            (
                i.id IS NULL OR
                ( i.active_dialogue = 0 AND i.expirydate > UTC_TIMESTAMP() )
            )
        WHERE c.is_active
        GROUP BY c.id
        ORDER BY c.name ASC
            """
        else:
            sql = """
        SELECT
            c.*,
            5 as numitems_total,
            1 as numitems_fromrefugees,
            4 as numitems_fromlocals
        FROM supdem_centre c LEFT JOIN supdem_item i
        ON
            i.centre_id = c.id AND
            (
                i.id IS NULL OR
                ( i.active_dialogue = 0 AND i.expirydate > datetime('now') )
            )
        WHERE c.is_active
        GROUP BY c.id
        ORDER BY c.name ASC
            """
        return cls.objects.raw(sql)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
            return self.name


# Does this table need a languagecode column as well?
class Item(models.Model):
    #poster = models.ForeignKey(MyUser)
    # centre is not a redundant field (yet) as the poster does not have a centre
    #centre = models.ForeignKey(Centre)
    # is_offer is not a redundant field (yet) as the poster does not have a usertype
    #is_offer = models.BooleanField()
    #active_dialogue = models.PositiveIntegerField(default=0, unique=False)
    creationdate = models.DateTimeField(auto_now_add=True)
    expirydate = models.DateTimeField()
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=200)
    description = models.TextField()
    owner = models.ForeignKey(MyUser)
    # image is semi-redundant. A photo id would have made more sense, but this
    # solution is much more efficient for showing lists of images
    image = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.title

    '''def for_usertype(self):
        return 'refugee' if self.is_offer else 'local'

    def url(self):
        return reverse('item', kwargs={
            'centreslug': self.centre.slug, 'usertype': self.for_usertype(), 'itemid': self.id
        })'''


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

from django import template
from django.db import models
from django.utils.translation import ugettext

register = template.Library()


# this is used as follows
# {% listtrans "cat" category.id %}
# this tag will be replaced by the category of the given id
# The second parameter can be an id or a Model object
@register.simple_tag
def listtrans(listname, id, name="name"):
    # If it is a model object, take the pk
    if isinstance(id, models.Model):
        id = id.pk
    return ugettext(listname + "-" + str(id) + "-" + name)

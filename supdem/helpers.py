from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.crypto import get_random_string
from datetime import datetime, timedelta
from .models import EmailLog, ResetPasswordKey


# todo jas: use https://docs.djangoproject.com/en/1.8/ref/utils/#django.utils.translation.activate
# at the beginning of this method and
# https://docs.djangoproject.com/en/1.8/ref/utils/#django.utils.translation.deactivate at the
# end to switch the locale for creating the  email. See also
# http://stackoverflow.com/questions/5258715/django-switching-for-a-block-of-code-switch-the-language-so-translations-are-d
def send_template_email(to_user, email_name, context={}, from_user=None):
    """" Send the email message with name email_name to to_user.

    The first line of the template should be "-- subject --", the second line should be the subject
    The third line should be "-- body txt --" and all following lines should be the body
    inspired by http://stackoverflow.com/a/28476681/5554831
    """
    # add some standard values to the context, render the template and split the lines
    context['fullname'] = to_user.username
    # if the tag ends with url, prepend it with the domain and remove the languagecode
    for name, value in context.items():
        if name[-3:] == 'url':
            context[name] = settings.DOMAIN_FOR_EMAILS + value

    # get the translated email
    cur_language = translation.get_language()
    #translation.activate(to_user.languagecode)
    rendered_template = render_to_string('supdem/email/' + email_name +
                                         '.txt', context).split('\n')
    translation.activate(cur_language)

    # todo jas: change from line parsing into a regexp so we can add an optional
    #    "-- body html --" block
    if rendered_template[0] != "-- subject --":
        raise ImproperlyConfigured("expect first line to be a subject indicator")
    if rendered_template[2] != "-- body txt --":
        raise ImproperlyConfigured("expect third line to be a body txt indicator")
    if from_user:
        status = send_mail(
            context['title'],
            context['message'],
            from_user.username+' <'+from_user.email + '>',
            [to_user.username + ' <' + to_user.email + '>']
        )
    else:
        status = send_mail(
            rendered_template[1],
            '\n'.join(rendered_template[3:]),
            settings.DEFAULT_FROM_EMAIL,
            [to_user.username + ' <' + to_user.email + '>']
        )

    EmailLog(
        email_name=email_name,
        to_user=to_user,
        status=status,
    ).save()
    return status


def reset(user):
    # delete old keys if they exist
    ResetPasswordKey.objects.filter(user=user).delete()
    newresetpasswordkey = ResetPasswordKey(
        user=user,
        key=get_random_string(20),
        expirydate=datetime.utcnow() + timedelta(hours=settings.PASSWORD_RESET_PERIOD_IN_HOURS)
    )
    newresetpasswordkey.save()
    send_template_email(user, 'password_reset', {
        'url': '/static/index.html#/password/' + newresetpasswordkey.key
    })

import os

from django.core.management.base import BaseCommand
from django.conf import settings

from supdem.models import Category, CategoryQuestion, CategoryQuestionOption, Centre


class Command(BaseCommand):
    help = 'create fake translation tags to fool manage.py makemessages'

    def handle(self, *args, **options):
        filename = os.path.join(settings.BASE_DIR, 'supdem', 'templates', 'supdem',
                                'this_is_only_for_gettext_generated.html')
        os.remove(filename)
        self.stdout.write('old file ' + filename + ' removed')
        f = open(filename, 'w')
        intro = """
This file is generated. It exists so manage.py makemessages
will create tage for list translations.
"""
        f.write(intro)

        self.stdout.write('Starting with categories')
        for cat in Category.objects.all():
            f.write("{# Translators: category '%s' #}\n" % cat.name_en)
            f.write("{%% trans 'cat-%s-name' %%}\n\n" % str(cat.id))

        self.stdout.write('Starting with categoryQuestions')
        for catque in CategoryQuestion.objects.all():
            f.write("{# Translators: Category Question '%s' #}\n" % catque.name_en)
            f.write("{%% trans 'catque-%s-name' %%}\n\n" % str(catque.id))

        self.stdout.write('Starting with CategoryQuestionOption')
        for catqueopt in CategoryQuestionOption.objects.all():
            f.write("{# Translators: Category Question option '%s' #}\n" % catqueopt.name_en)
            f.write("{%% trans 'catqueopt-%s-name' %%}\n\n" % str(catqueopt.id))

        self.stdout.write('Starting with Centre')
        for centre in Centre.objects.all():
            f.write("{# Translators: Centre message for locals near '%s' #}\n" % centre.name)
            f.write("{%% trans 'cen-%s-message_for_locals' %%}\n\n" % str(centre.id))
            f.write("{# Translators: Centre message for refugees near '%s' #}\n" % centre.name)
            f.write("{%% trans 'cen-%s-message_for_refugees' %%}\n\n" % str(centre.id))

        f.close()
        self.stdout.write('All done, file closed')

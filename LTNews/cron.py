from django_cron import CronJobBase, Schedule
from collections import Counter

from Application.utilities.populate_utilities import update_feed
from Application.service.feed_services import all_feeds_link
from Application.service.profile_services import all_profile, get_filtered_status_by_profile
from Application.service.item_services import get_item_keywords

from Application.models import Keyword
from django.utils import timezone
import traceback


class UpdateRSS(CronJobBase):
    RUN_EVERY_MINS = 60
    RETRY_AFTER_FAILURE_MINS = 5

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS,
                        retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'cron.UpdateRSS'

    def do(self):
        print("INI CRON1 - Actualizando entradas ({})".format(timezone.now()))
        for link in all_feeds_link():
            try:
                update_feed(link['link_rss'], printer=True)
            except:
                print(traceback.format_exc())
                print("Error de cron")
        pass
        print("FIN CRON1 - Actualizando entradas ({})".format(timezone.now()))
    pass


class CalculeKeywords(CronJobBase):
    RUN_EVERY_MINS = 1440
    RETRY_AFTER_FAILURE_MINS = 30

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS,
                        retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'cron.CalculeKeywords'

    def do(self):
        print('INI CRON2 - Calculando keywords por cada usuario ({})'.format(timezone.now()))

        for profile in all_profile():
            print('\tINI {}'.format(profile.user.username))
            cont_user = Counter()
            for status in get_filtered_status_by_profile(profile.id):
                for tag in get_item_keywords(status.item.id, status.item.get_key_number()):
                    cont_user[tag] += status.get_score()

            Keyword.objects.filter(users__id=profile.id).delete()

            for tag_x in cont_user.most_common(8):
                keyword, created = Keyword.objects.get_or_create(term=tag_x[0])
                keyword.users.add(profile)
                keyword.save()

            print('\tFIN {}'.format(profile.user.username))
        pass

        print('FIN CRON2 - Calculando keywords por cada usuario ({})'.format(timezone.now()))
    pass

from django_cron import CronJobBase, Schedule
from collections import Counter

from Application.utilities.populate_utilities import update_feed
from Application.utilities.python_utilities import floor_log
from Application.utilities.recommend_utilities import get_recommendations
from Application.service.feed_services import all_feeds_link
from Application.service.profile_services import all_profile, get_filtered_status_by_profile
from Application.service.item_services import get_item

from Application.models import Keyword
from django.utils import timezone
import traceback


class UpdateRSS(CronJobBase):
    RUN_EVERY_MINS = 30
    RETRY_AFTER_FAILURE_MINS = 5

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS,
                        retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'cron.UpdateRSS'

    @staticmethod
    def do():
        print("INI CRON1 - Actualizando entradas ({})".format(timezone.now()))
        for link in all_feeds_link():
            try:
                update_feed(link['link_rss'], printer=True)
            except Exception:
                print(traceback.format_exc())
                print("Error de cron")

        print("FIN CRON1 - Actualizando entradas ({})".format(timezone.now()))


class CalculateKeywords(CronJobBase):
    RUN_EVERY_MINS = 1440
    RETRY_AFTER_FAILURE_MINS = 30

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS,
                        retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'cron.CalculeKeywords'

    @staticmethod
    def do():
        print('INI CRON2 - Calculando keywords por cada usuario ({})'.format(timezone.now()))

        print('\tBasado en contenido')
        critics = dict()
        for profile in all_profile():
            print('\t\tINI {}'.format(profile.user.username))

            try:
                cont_user = Counter()
                critics.setdefault(profile.id, {})

                for status in get_filtered_status_by_profile(profile.id):
                    for tag in get_item(status.item.id).keywords.all():
                        critics[profile.id][tag.term] = float(status.get_score())
                        cont_user[tag.term] += status.get_score()

                Keyword.objects.filter(users__id=profile.id).delete()
                number = floor_log(len(cont_user))

                for tag_x in cont_user.most_common(number):
                    keyword = Keyword.objects.get_or_create(term=tag_x[0])[0]
                    keyword.users.add(profile)
                    keyword.save()
            except Exception:
                print(traceback.format_exc())
                print("Error de cron")

            print('\t\tFIN {}'.format(profile.user.username))

        print('\tFiltro Colaborativo')
        for profile in all_profile():
            print('\t\tINI {}'.format(profile.user.username))

            try:
                for recommend in get_recommendations(critics, profile.id)[:2]:
                    print(recommend)
                    keyword = Keyword.objects.get_or_create(term=recommend)[0]
                    keyword.users.add(profile)
                    keyword.save()
            except Exception:
                print(traceback.format_exc())
                print("Error de cron")

            print('\t\tFIN {}'.format(profile.user.username))

        print('FIN CRON2 - Calculando keywords por cada usuario ({})'.format(timezone.now()))

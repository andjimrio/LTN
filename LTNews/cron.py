from django_cron import CronJobBase, Schedule
from collections import Counter

from Application.utilities.index_utilities import get_item_keywords
from Application.utilities.populate_utilities import update_feed
from Application.utilities.queries_utilities import all_feeds_link, all_profile, \
    get_filtered_status_by_profile

from Application.models import Keyword


class UpdateRSS(CronJobBase):
    RUN_EVERY_MINS = 60
    RETRY_AFTER_FAILURE_MINS = 5

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS,
                        retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'cron.UpdateRSS'

    def do(self):
        print("Actualizando entradas")
        for link in all_feeds_link():
            try:
                update_feed(link['link_rss'], printer=True)
            except:
                print("Error de cron")
        pass
    pass


class CalculeKeywords(CronJobBase):
    RUN_EVERY_MINS = 1440
    RETRY_AFTER_FAILURE_MINS = 30

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS,
                        retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'cron.CalculeKeywords'

    def do(self):
        print('Calculando keywords por cada usuario')

        for profile in all_profile():
            print('INI {}'.format(profile.user.username))
            cont_user = Counter()
            for status in get_filtered_status_by_profile(profile.id):
                for tag in get_item_keywords(status.item.id, status.item.get_key_number()):
                    cont_user[tag] += status.get_score()

            Keyword.objects.filter(users__user_id=profile.id).delete()

            for tag_x in cont_user.most_common(8):
                keyword, created = Keyword.objects.get_or_create(term=tag_x)
                keyword.users.add(profile)
                keyword.save()

            print('FIN {}'.format(profile.user.username))
        pass
    pass

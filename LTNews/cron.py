from django.core import management
from django_cron import CronJobBase, Schedule

from Application.utilities.populate_utilities import populate_rss
from Application.utilities.queries_utilities import all_feeds_link


class cron_update_rss(CronJobBase):
    RUN_EVERY_MINS = 60 # every 1 hours
    RETRY_AFTER_FAILURE_MINS = 5

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'cron.cron_update_rss'    # a unique code

    def do(self):
        print("Actualizando entradas")
        for link in all_feeds_link():
            try:
                populate_rss(link['link'], printer=True)
                #update_rss(ide['id'], printer=True)
            except:
                print("Error de cron")

        try:
            management.call_command('update_index')
        except:
            print("Error de haystack")

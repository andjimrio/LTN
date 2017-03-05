from django_cron import CronJobBase, Schedule

class update_rss(CronJobBase):
    RUN_EVERY_MINS = 600 # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'Application.my_cron_job'    # a unique code

    def do(self):
        print("Hola")
        pass    # do your thing here
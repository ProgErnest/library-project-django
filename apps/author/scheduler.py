# from apscheduler.schedulers.background import BackgroundScheduler
# from django_apscheduler.jobstores import DjangoJobStore
# from django.core.management import call_command

# def run_nofify_late():
#     call_command("notify_late")
# def start_plannificator():
#     scheduler = BackgroundScheduler()
#     scheduler.add_jobstore(DjangoJobStore(),"default")
#     scheduler.add_job(
#         run_nofify_late,
#         trigger="interval", 
#         seconds=30,
#         id="notify_late_job",
#         replace_existing=True

#     )
#     scheduler.start()
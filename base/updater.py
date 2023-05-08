from apscheduler.schedulers.background import BackgroundScheduler
from .background import man_unpin_posts, man_archive_posts, man_publish_posts


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(man_unpin_posts, 'interval', minutes=1)
    scheduler.add_job(man_archive_posts, 'interval', minutes=1)
    scheduler.add_job(man_publish_posts, 'interval', minutes=1)
    scheduler.start()
from crontab import CronTab
import os


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


def start_job():
    cron = CronTab(user=True)
    command = os.path.join(PROJECT_ROOT, "venv/bin/python " + os.path.join(PROJECT_ROOT, "kostal_db_fill.py"))
    job1 = cron.new(command=command, comment="THISISPV")

    job1.minute.every(1)
    cron.write()
    return None


if __name__ == "__main__":
    start_job()

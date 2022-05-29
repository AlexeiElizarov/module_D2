
import logging
from datetime import date, datetime, timedelta

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution


import sys


sys.path.append('/project/newspaper')
from newspaper.models import Category, Post



logger = logging.getLogger(__name__)



def my_job():
    for name_category in Category.objects.all():
        print('start')
        users_subscribers = User.objects.filter(subscribe=name_category)
        today = date.today()
        seven_day_before = today - timedelta(days=7)
        posts = Post.objects.filter(date__gte=seven_day_before,
                                     post_category__category=name_category)
        print(posts)
        email_users_subscribers = [u.email for u in users_subscribers]
        html_content = render_to_string(
            'newspaper/email_week.html',
            {'posts': posts, 'name_category': name_category})
        msg = EmailMultiAlternatives(
            subject=f'{name_category}',
            body=f"Новый пост",
            from_email='Lafen55@yandex.ru',
            to=email_users_subscribers,
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    # send_mail(
    #     subject=f'django',
    #     # имя клиента и дата записи будут в теме для удобства
    #     message='hello',  # сообщение с кратким описанием проблемы
    #     from_email='Lafen55@yandex.ru',  # здесь указываете почту, с которой будете отправлять (об этом попозже)
    #     recipient_list=['alexeiasd2@gmail.com']  # здесь список получателей. Например, секретарь, сам врач и так далее
    # )


# функция которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),#second="*/10"
            # Тоже самое что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
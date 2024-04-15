from datetime import datetime, date, timedelta

import requests
from celery import shared_task
from django.conf import settings

from habits.models import Habit


@shared_task
def send_reminder_about_habit():
    """
    Отправка пользователю в Телеграм напоминания о привычке
    """

    URL = 'https://api.telegram.org/bot'
    TOKEN = settings.TELEGRAM_TOKEN

    time_now = datetime.now().time().replace(second=0, microsecond=0)
    date_now = date.today()
    habits_to_send = Habit.objects.filter(is_pleasant=False)

    for habit in habits_to_send:
        if habit.date == date_now or not habit.date:
            if habit.time >= time_now:
                chat_id = habit.owner.telegram_id
                text = f"Вам нужно {habit.action} в {habit.time} в {habit.place}"
                url = f"{URL}{TOKEN}/sendMessage"
                data_post = {"chat_id": chat_id, "text": text}
                requests.post(url=url, data=data_post)
            habit.date = date_now + timedelta(days=habit.periodicity)
            habit.save()
